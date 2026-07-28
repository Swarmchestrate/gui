"""Gather the database rows a capacity template is built from.

The GUI does not assemble TOSCA. It collects the capacity's rows and posts them
keyed by table name; SAT Builder reads the profile's gui_name bindings to decide
where each column belongs. Adding a field to the profile therefore needs no
change here, as long as its column is in one of the tables below.
"""
from postgrest.api import ApiClient
from postgrest.table_names import TableNames
from resource_management.tosca import generate_sat


# Child tables holding one row per instance flavour, or several rows per
# capacity, keyed by their foreign key back to the capacity.
CHILD_TABLES = {
    TableNames.CAPACITY_INSTANCE_TYPE: "capacity_id",
    TableNames.CAPACITY_PORT_RULE: "capacity_id",
}

# Tables the capacity row points at, keyed by the column holding the reference.
REFERENCED_TABLES = {
    "locality_id": TableNames.LOCALITY,
    "resource_quota_id": TableNames.CAPACITY_RESOURCE_QUOTA,
}

# Which node types SAT Builder should instantiate. A capacity's node type is
# decided by two columns: resource_type separates cloud from edge, and cloud
# picks the platform. Each platform is a distinct TOSCA type with its own
# properties, so adding one means a new value here plus its columns.
EDGE_NODE_TYPE = "EdgeCapacity"
CLOUD_TO_NODE_TYPE = {
    "aws": "EC2Capacity",
    "openstack": "OpenStackCapacity",
}

# Always requested; SAT Builder omits it when the payload has no quota data.
TOTALS_NODE_TYPE = "OverallCapacity"


def build_capacity_payload(capacity_id: int) -> dict:
    """Collect every row that contributes to a capacity template."""
    api_client = ApiClient()
    api_client.initialise_openapi_spec()

    capacity_endpoint = api_client.get_endpoint(TableNames.CAPACITY_NEW)
    capacity = capacity_endpoint.get(capacity_id).as_dict()

    payload = {TableNames.CAPACITY_NEW.value: capacity}

    for column_name, table_name in REFERENCED_TABLES.items():
        referenced_id = capacity.get(column_name)
        if not referenced_id:
            continue
        endpoint = api_client.get_endpoint(table_name)
        payload[table_name.value] = endpoint.get(referenced_id).as_dict()

    for table_name, foreign_key in CHILD_TABLES.items():
        endpoint = api_client.get_endpoint(table_name)
        rows = endpoint.get_resources_referencing_resource_id(foreign_key, capacity_id)
        if rows:
            payload[table_name.value] = [row.as_dict() for row in rows]

    return payload


def node_types_for(capacity: dict) -> list[str]:
    """Pick the node type from the capacity's resource type and cloud platform."""
    resource_type = (capacity.get("resource_type") or "").strip().lower()

    if resource_type == "edge":
        return [EDGE_NODE_TYPE, TOTALS_NODE_TYPE]

    if resource_type == "cloud":
        cloud = (capacity.get("cloud") or "").strip().lower()
        node_type = CLOUD_TO_NODE_TYPE.get(cloud)
        if not node_type:
            supported = ", ".join(sorted(CLOUD_TO_NODE_TYPE))
            raise ValueError(
                f"Cloud capacity '{capacity.get('name')}' has cloud "
                f"'{capacity.get('cloud')}', which has no TOSCA node type. "
                f"Expected one of: {supported}."
            )
        return [node_type, TOTALS_NODE_TYPE]

    raise ValueError(
        f"Capacity '{capacity.get('name')}' has resource type "
        f"'{capacity.get('resource_type')}'. Expected Cloud or Edge."
    )


def generate_cdt_yaml(capacity_id: int) -> str:
    """Build the Capacity Description Template for a capacity."""
    payload = build_capacity_payload(capacity_id)
    params = {
        "node_types": node_types_for(payload[TableNames.CAPACITY_NEW.value]),
        "response_type": "yaml",
    }
    return generate_sat(payload, params, "capacity/build")
