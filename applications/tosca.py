"""Gather the database rows an application template is built from.

The GUI does not assemble TOSCA. It collects the application's rows and posts
them keyed by table name; SAT Builder reads the profile's gui_name bindings to
decide where each column belongs. Adding a field to the profile therefore needs
no change here, as long as its column is in one of the tables below.

Only the commonly used properties have a column of their own. Anything else the
profile declares is reached through application_property, whose rows name the
property they set - so a user is not limited to the fields the form offers.
"""
import logging

from postgrest.api import ApiClient
from postgrest.table_names import TableNames
from resource_management.tosca import generate_sat


logger = logging.getLogger(__name__)

# Tables holding one row per microservice, keyed by their foreign key back to
# the application.
MICROSERVICE_TABLES = {
    TableNames.APPLICATION_MICROSERVICE: "application_id",
}

# Tables hanging off each microservice rather than off the application. SAT
# Builder scopes their rows by application_microservice_id, so every
# microservice's node template gets only its own.
PER_MICROSERVICE_TABLES = (
    TableNames.APPLICATION_ENVIRONMENT_VAR,
    TableNames.APPLICATION_SECURITY_RULE,
    TableNames.APPLICATION_PROPERTY,
)

MICROSERVICE_FOREIGN_KEY = "application_microservice_id"

# One node template per microservice. There is a single application node type,
# so unlike a capacity there is nothing to choose between.
MICROSERVICE_NODE_TYPE = "Microservice"


def build_application_payload(application_id: int) -> dict:
    """Collect every row that contributes to an application template."""
    api_client = ApiClient()
    api_client.initialise_openapi_spec()

    application_endpoint = api_client.get_endpoint(TableNames.APPLICATION_NEW)
    application = application_endpoint.get(application_id).as_dict()

    payload = {TableNames.APPLICATION_NEW.value: application}

    microservice_ids = []
    for table_name, foreign_key in MICROSERVICE_TABLES.items():
        endpoint = api_client.get_endpoint(table_name)
        rows = endpoint.get_resources_referencing_resource_id(foreign_key, application_id)
        if not rows:
            continue
        payload[table_name.value] = [row.as_dict() for row in rows]
        microservice_ids.extend(row.pk for row in rows)

    for table_name in PER_MICROSERVICE_TABLES:
        if not _table_exists(api_client, table_name):
            # application_property is optional: an installation that has not
            # created it yet should still build a template from the rest.
            logger.warning("No '%s' table; skipping it in the payload", table_name.value)
            continue
        rows = _rows_for_microservices(api_client, table_name, microservice_ids)
        if rows:
            payload[table_name.value] = rows

    return payload


def _table_exists(api_client: ApiClient, table_name: TableNames) -> bool:
    return bool(api_client.openapi_spec.get_definition(table_name.value).as_dict())


def _rows_for_microservices(
        api_client: ApiClient,
        table_name: TableNames,
        microservice_ids: list) -> list[dict]:
    """Rows of a per-microservice table, for every microservice at once."""
    endpoint = api_client.get_endpoint(table_name)
    rows = []
    for microservice_id in microservice_ids:
        rows.extend(
            row.as_dict() for row in
            endpoint.get_resources_referencing_resource_id(
                MICROSERVICE_FOREIGN_KEY, microservice_id
            )
        )
    return rows


def generate_adt_yaml(application_id: int) -> str:
    """Build the Application Description Template for an application."""
    payload = build_application_payload(application_id)
    params = {
        "node_types": [MICROSERVICE_NODE_TYPE],
        "response_type": "yaml",
    }
    return generate_sat(payload, params, "application/build")
