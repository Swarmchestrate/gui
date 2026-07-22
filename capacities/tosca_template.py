import json
import os
import yaml

from django.conf import settings
from django.template import Template, Context

from postgrest.api import ApiClient
from postgrest.table_names import TableNames
from resource_management.tosca import generate_sat


BASE_DIR = settings.BASE_DIR


def get_data_for_cdt(capacity_id: int) -> dict:
    capacity_id = int(capacity_id)
    # Set up API client
    api_client = ApiClient()
    api_client.initialise_openapi_spec()
    # Capacity
    endpoint = api_client.get_endpoint(TableNames.CAPACITY_NEW)
    capacity = endpoint.get(capacity_id)
    capacity_dict = capacity.as_dict()
    # Capacity - Operating Systems
    capacity_operating_system_endpoint = api_client.get_endpoint(TableNames.CAPACITY_OPERATING_SYSTEM)
    capacity_operating_systems = capacity_operating_system_endpoint.get_resources_by_params({
        "capacity_id": capacity_id,
    })
    capacity_operating_system_dicts = [
        capacity_operating_system.as_dict()
        for capacity_operating_system in capacity_operating_systems
    ]
    # Capacity - Instance Types
    capacity_instance_type_endpoint = api_client.get_endpoint(TableNames.CAPACITY_INSTANCE_TYPE)
    capacity_instance_types = capacity_instance_type_endpoint.get_resources_by_params({
        "capacity_id": capacity_id,
    })
    capacity_instance_type_dicts = [
        capacity_instance_type.as_dict()
        for capacity_instance_type in capacity_instance_types
    ]
    # Locality
    locality_endpoint = api_client.get_endpoint(TableNames.LOCALITY)
    locality_id = capacity.as_dict().get("locality_id")
    locality_dict = None
    if locality_id:
        locality = locality_endpoint.get(locality_id)
        locality_dict = locality.as_dict()
    return {
        "capacity": capacity_dict,
        "capacity_operating_systems": capacity_operating_system_dicts,
        "capacity_instance_types": capacity_instance_type_dicts,
        "locality": locality_dict,
    }


def generate_cdt_yaml(capacity_id: int) -> str | None:
    data = get_data_for_cdt(capacity_id)
    cdt_template_path = os.path.join(
        BASE_DIR,
        "capacities",
        "cdt_template.yaml.djt"
    )
    cdt_template_string = ""
    with open(cdt_template_path, "r") as cdt_template_file:
        cdt_template_string = cdt_template_file.read()
    template = Template(cdt_template_string)
    context = Context(data)
    data_yaml = template.render(context)
    yaml_as_dict = yaml.safe_load(data_yaml)
    data_json = json.dumps(yaml_as_dict, indent=4, default=str)
    capacity_description = "This Capacity Description Template was generated using the Swarmchestrate GUI."
    if data.get("capacity").get("description"):
        capacity_description = data.get("capacity").get("description")
    params = {
        # "response_type": "yaml_and_json",
        "template_version": "latest",
        # "definitions_version": "tosca_3_1",
        "description": capacity_description,
    }
    cdt = generate_sat(
        data_json,
        params,
        "capacity/build"
    )
    return yaml.dump(cdt, default_flow_style=False)