import yaml

from postgrest.api import ApiClient


def generate_capacity_description_template(capacity_id: int) -> str:
    api_client = ApiClient()
    api_client.initialise_openapi_spec()
    endpoint = api_client.get_endpoint("capacity_new")
    capacity_as_dict = endpoint.get(capacity_id).as_dict()
    return yaml.dump(capacity_as_dict, default_flow_style=False)