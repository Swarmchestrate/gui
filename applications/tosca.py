import json
import yaml

from django.conf import settings

from postgrest.api import ApiClient
from postgrest.table_names import TableNames
from resource_management.tosca import generate_sat


def generate_adt_yaml(application_id: int) -> str | None:
    api_client = ApiClient()
    api_client.initialise_openapi_spec()
    endpoint = api_client.get_endpoint(TableNames.APPLICATION_NEW)
    data = endpoint.get(application_id).as_dict()
    data = json.dumps(data, indent=4)
    params = {
        "response_type": "yaml",
        "template_version": "001",
        "definitions_version": "tosca_1_0",
        "description": "test"
    }
    sat = generate_sat(
        data,
        params,
        "application/build"
    )
    return yaml.dump(sat, default_flow_style=False)