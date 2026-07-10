import json
import operator
import yaml
from functools import reduce

from postgrest.api import ApiClient
from postgrest.table_names import TableNames
from resource_management.exceptions import NameMissingException
from resource_management.tosca import generate_sat


capacity_to_cdt_base_mappings = {
    "name": ["metadata", "name"],
    "quota": ["capabilities", "capacity", "instances"],
}

capacity_to_cdt_node_types_mappings = {
    "resource_provider": ["resource", "provider"],
    "capacity_provider": ["resource", "capacity-provider"],
    "resource_type": ["resource", "type"],
    "energy_type": ["energy", "energy-type"],
    "powered_type": ["energy", "powered-type"],
    "trust": ["trust", "level"],
    "bandwidth_mbps": ["host", "bandwidth"],
    "connectivity_type": ["network", "type"],
}

instance_type_to_cdt_node_types_mappings = {
    "quota": ["capacity", "instances"],
}


# Credit for "get_by_path" and "set_by_path":
# https://stackoverflow.com/a/14692747
def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


def set_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value


def setup_path(
        cdt: dict,
        items: list):
    # Set up a dict at each path item.
    for i, item in enumerate(items):
        sub_items = items[:i]
        if not sub_items:
            continue
        try:
            get_by_path(cdt, sub_items)
            # Continue if a path has already been set up.
            continue
        except KeyError:
            pass
        set_by_path(cdt, items[:i], {})
    set_by_path(cdt, items, {})
    return cdt


def add_data_to_cdt(
        cdt: dict,
        data: str,
        mappings: dict):
    for key, path in mappings.items():
        value = data.get(key)
        if not value:
            continue
        setup_path(cdt, path)
        set_by_path(cdt, path, value)
    return cdt


def add_metadata_to_cdt(
        cdt: dict,
        data: dict) -> dict:
    cdt["metadata"] = {
        "name": "Swarmchestrate CDT",
    }
    return cdt


def add_base_resource_type(
        cdt: dict,
        data: dict) -> dict:
    base_resource_type_name = data.get("name")
    if not base_resource_type_name:
        raise NameMissingException(f"Please specify a name for this capacity in the wizard.")
    mappings = {
        "name": ["node_types", base_resource_type_name, "name"],
        "description": ["node_types", base_resource_type_name, "description"],
    }
    add_data_to_cdt(cdt, data, mappings)
    return cdt


def add_locality_to_cdt(
        cdt: dict,
        data: dict,
        base_resource_type_name: str) -> dict:
    mappings = {
        "continent": [
            "node_types",
            base_resource_type_name,
            "capabilities",
            "host",
            "locality",
            "continent",
            "default",
        ],
        "country": [
            "node_types",
            base_resource_type_name,
            "capabilities",
            "host",
            "locality",
            "country",
            "default",
        ],
        "city": [
            "node_types",
            base_resource_type_name,
            "capabilities",
            "host",
            "locality",
            "city",
            "default",
        ],
    }
    add_data_to_cdt(cdt, data, mappings)
    return cdt


def add_capacity_flavours_to_cdt(
        cdt: dict,
        data: dict) -> dict:
    setup_path(cdt, ["service_template", "node_templates"])
    return cdt


def add_capacity_data_to_cdt(
        cdt: dict,
        data: dict) -> dict:
    pass


def map_to_cdt_format(data: dict) -> dict:
    cdt = {
        "metadata": {
            # name, created_at, updated_at...
        },
        "node_types": {
            # common properties across capacity flavours
        },
    }
    # Define metadata
    cdt = add_metadata_to_cdt(cdt, data)
    # Define a base resource type
    # node_types / <capacity_name>
    cdt = add_base_resource_type(cdt, data)
    # Define flavours (capacity_instance_type)
    cdt = add_capacity_flavours_to_cdt(cdt, data)
    return cdt


def generate_cdt_yaml(capacity_id: int) -> str | None:
    api_client = ApiClient()
    api_client.initialise_openapi_spec()
    endpoint = api_client.get_endpoint(TableNames.CAPACITY_NEW)
    unformatted_data = endpoint.get(capacity_id).as_dict()
    data = map_to_cdt_format(unformatted_data)
    locality_endpoint = api_client.get_endpoint(TableNames.LOCALITY)
    locality_id = unformatted_data.get("locality_id")
    if locality_id:
        locality = locality_endpoint.get(locality_id)
        data = add_locality_to_cdt(
            data,
            locality.as_dict(),
            unformatted_data.get("name")
        )
    params = {
        "response_type": "json",
        "template_version": "003",
        "definitions_version": "tosca_3_1",
        "description": "This Capacity Description Template was generated using the Swarmchestrate GUI.",
    }
    data_json = json.dumps(data, indent=4)
    cdt = generate_sat(
        data_json,
        params,
        "capacity/build"
    )
    return yaml.dump(cdt, default_flow_style=False)