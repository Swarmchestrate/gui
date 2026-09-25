import hashlib
import json
import logging
import os
import requests
from dataclasses import dataclass

from postgrest.api_configs.base_config import build_api_url
from .exceptions import SatBuilderException


logger = logging.getLogger(__name__)

# Where a capacity or application records the data that last passed validation.
# It is the GUI's bookkeeping, not part of any template.
VALIDATED_FINGERPRINT_COLUMN = "validated_fingerprint"

# Columns that change without the template changing, so they must not make
# validated data look edited.
_COLUMNS_OUTSIDE_FINGERPRINT = {VALIDATED_FINGERPRINT_COLUMN, "updated_at"}


@dataclass
class TemplateRequest:
    """Everything SAT Builder is sent to build one template."""
    payload: dict
    params: dict
    endpoint_path: str

    def generate(self) -> str:
        return generate_sat(self.payload, self.params, self.endpoint_path)

    def fingerprint(self) -> str:
        """Identify this exact data, so a later build can tell if it changed.

        Row order is not part of it: PostgREST does not promise one, and the
        same rows in a different order are the same template.
        """
        def row(values):
            return {
                column: value for column, value in values.items()
                if column not in _COLUMNS_OUTSIDE_FINGERPRINT
            }

        payload = {}
        for table_name, rows in self.payload.items():
            if isinstance(rows, list):
                payload[table_name] = sorted(
                    (row(r) for r in rows),
                    key=lambda r: json.dumps(r, sort_keys=True, default=str),
                )
            else:
                payload[table_name] = row(rows)
        blob = json.dumps(
            {"endpoint": self.endpoint_path, "params": self.params, "payload": payload},
            sort_keys=True,
            default=str,
        )
        return hashlib.sha256(blob.encode()).hexdigest()


def without_validation_bookkeeping(row: dict) -> dict:
    """The row as template data, without the column recording its validation."""
    return {k: v for k, v in row.items() if k != VALIDATED_FINGERPRINT_COLUMN}


def generate_sat(
        payload: dict,
        params: dict,
        endpoint_path: str) -> str:
    """Build a template from database rows and return it as YAML.

    The payload is rows keyed by table name. SAT Builder reads the TOSCA
    profile to decide where each column belongs, so nothing here needs to know
    the shape of the template being produced.
    """
    response = requests.post(
        build_api_url(
            os.environ.get("SAT_BUILDER_API_URL"),
            endpoint_path,
            env_var_name="SAT_BUILDER_API_URL"
        ),
        headers={"Content-Type": "application/json"},
        params=params,
        data=json.dumps(payload)
    )

    if response.status_code == 422:
        problems = _validation_problems(response)
        raise SatBuilderException(_describe_validation_failure(problems), problems)
    if not response.ok:
        raise SatBuilderException(
            f"SAT Builder returned {response.status_code}: {response.text[:200]}"
        )

    body = response.json()
    for warning in body.get("warnings") or []:
        logger.warning("SAT Builder: %s", "; ".join(str(v) for v in warning.values()))

    template_yaml = body.get("template_yaml")
    if not template_yaml:
        raise SatBuilderException("SAT Builder returned no template")
    return template_yaml


def _validation_problems(response) -> list[str]:
    """Turn SAT Builder's field-level errors into lines a user can act on."""
    try:
        details = response.json().get("detail") or []
    except ValueError:
        return [f"SAT Builder rejected the request: {response.text[:200]}"]
    if isinstance(details, str):
        return [details]

    missing = [d for d in details if isinstance(d, dict) and d.get("kind") == "missing"]
    others = [d for d in details if isinstance(d, dict) and d.get("kind") != "missing"]

    problems = []
    if missing:
        fields = ", ".join(sorted({d["path"].split(".")[-1] for d in missing}))
        problems.append(f"Missing required values: {fields}.")
    problems.extend(detail.get("message", str(detail)) for detail in others)
    return problems


def _describe_validation_failure(problems: list[str]) -> str:
    """Summarise the problems in one message for the wizard."""
    # The missing values, if any, come first and are always kept.
    return " ".join(problems[:6]) or "SAT Builder rejected the request."