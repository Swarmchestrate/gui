"""Whether a capacity's or application's current data has passed validation.

A template can only be downloaded once SAT Builder has accepted it. What was
accepted is recorded on the record itself, as a fingerprint of the exact data
sent, so every user sees the same state. Any edit clears it, and a download
checks the data still matches it.
"""
import logging

from django.http import HttpRequest

from postgrest.api import ApiClient
from postgrest.table_names import TableNames
from .tosca import VALIDATED_FINGERPRINT_COLUMN


logger = logging.getLogger(__name__)

# The tables a template is built from the rows of.
TEMPLATE_TABLES = {TableNames.CAPACITY_NEW.value, TableNames.APPLICATION_NEW.value}

_READ_ONLY_METHODS = {"GET", "HEAD", "OPTIONS", "TRACE"}


def record_validation(table_name: str, resource_id, fingerprint: str | None):
    """Store the fingerprint of validated data, or None to clear it."""
    api_client = ApiClient()
    api_client.initialise_openapi_spec()
    endpoint = api_client.get_endpoint(table_name)
    if not endpoint.definition.has_column(VALIDATED_FINGERPRINT_COLUMN):
        logger.warning(
            "No '%s' column on '%s'; validation cannot be recorded",
            VALIDATED_FINGERPRINT_COLUMN, table_name,
        )
        return
    endpoint.update(resource_id, {VALIDATED_FINGERPRINT_COLUMN: fingerprint})


def validated_fingerprint(resource: dict | None) -> str | None:
    return (resource or {}).get(VALIDATED_FINGERPRINT_COLUMN) or None


class ClearValidationOnEditMiddleware:
    """Clear a record's validation whenever a request may have edited it.

    Every edit, from the wizard's autosave to adding or deleting a child row,
    is a write to a URL naming the capacity or application it belongs to. The
    record is cleared whether or not the edit succeeded: validating again is
    cheap, and downloading data that was never validated is what this prevents.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        if request.method not in _READ_ONLY_METHODS:
            self._clear_for(request)
        return response

    def _clear_for(self, request: HttpRequest):
        match = getattr(request, "resolver_match", None)
        if match is None:
            return
        view_class = getattr(match.func, "view_class", None)
        if getattr(view_class, "keeps_template_validation", False):
            return
        # The postgrest views take the table from the URL; the rest are
        # dedicated to one table.
        table_name = match.kwargs.get("table_name") or getattr(view_class, "table_name", None)
        resource_id = match.kwargs.get("resource_id")
        if resource_id is None or str(table_name) not in TEMPLATE_TABLES:
            return
        try:
            record_validation(str(table_name), resource_id, None)
        except Exception:
            # The edit itself has happened; a download still checks the data
            # against what was validated, so this must not fail the request.
            logger.exception(
                "Could not clear the validation of %s %s", table_name, resource_id
            )
