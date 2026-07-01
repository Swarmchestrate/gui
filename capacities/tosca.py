import json
import yaml

from django.conf import settings

from postgrest.api import ApiClient
from postgrest.table_names import TableNames
from resource_management.tosca import generate_sat


def generate_cdt_yaml(capacity_id: int) -> str | None:
    api_client = ApiClient()
    api_client.initialise_openapi_spec()
    endpoint = api_client.get_endpoint(TableNames.CAPACITY_NEW)
    data = endpoint.get(capacity_id).as_dict()
    data = json.dumps(data, indent=4)
    params = {
        "response_type": "json",
        "template_version": "003",
        "definitions_version": "tosca_3_1",
        "description": "test"
    }
    sat = generate_sat(
        data,
        params,
        "capacity/build"
    )
    return yaml.dump(sat, default_flow_style=False)