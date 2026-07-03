import json
import yaml

from postgrest.api import ApiClient
from postgrest.table_names import TableNames
from resource_management.exceptions import DescriptionMissingException
from resource_management.tosca import generate_sat


def map_to_sat_builder_api_format(data: dict):
    formatted_data = {
        "metadata": {},
        "service_template": {
            "node_templates": {},
        },
    }
    if data.get("name"):
        formatted_data["metadata"].update({
            "name": data.get("name"),
        })
    return json.dumps(formatted_data, indent=4)


def generate_cdt_yaml(capacity_id: int) -> str | None:
    api_client = ApiClient()
    api_client.initialise_openapi_spec()
    endpoint = api_client.get_endpoint(TableNames.CAPACITY_NEW)
    unformatted_data = endpoint.get(capacity_id).as_dict()
    description = unformatted_data.get("description")
    if not description:
        raise DescriptionMissingException(f"Please specify a description for Capacity {capacity_id} in the wizard.")
    data = map_to_sat_builder_api_format(unformatted_data)
    params = {
        "response_type": "json",
        "template_version": "003",
        "definitions_version": "tosca_3_1",
        "description": description,
    }
    sat = generate_sat(
        data,
        params,
        "capacity/build"
    )
    return yaml.dump(sat, default_flow_style=False)