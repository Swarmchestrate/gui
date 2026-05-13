import yaml

from postgrest.api import ApiClient


def generate_application_description_template(application_id: int) -> str:
    api_client = ApiClient()
    api_client.initialise_openapi_spec()
    endpoint = api_client.get_endpoint("application_new")
    application_as_dict = endpoint.get(application_id).as_dict()
    return yaml.dump(application_as_dict, default_flow_style=False)