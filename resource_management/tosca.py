import json
import logging
import os
import requests

from postgrest.api_configs.base_config import build_api_url
from .exceptions import SatBuilderException


logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)


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
        raise SatBuilderException(_describe_validation_failure(response))
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


def _describe_validation_failure(response) -> str:
    """Turn SAT Builder's field-level errors into a message for the wizard."""
    try:
        details = response.json().get("detail") or []
    except ValueError:
        return f"SAT Builder rejected the request: {response.text[:200]}"

    missing = [d for d in details if isinstance(d, dict) and d.get("kind") == "missing"]
    others = [d for d in details if isinstance(d, dict) and d.get("kind") != "missing"]

    lines = []
    if missing:
        fields = ", ".join(sorted({d["path"].split(".")[-1] for d in missing}))
        lines.append(f"Missing required values: {fields}.")
    for detail in others[:5]:
        lines.append(detail.get("message", str(detail)))
    return " ".join(lines) or "SAT Builder rejected the request."
