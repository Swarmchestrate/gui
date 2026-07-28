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
    TableNames.CAPACITY_OPERATING_SYSTEM: "capacity_id",
    TableNames.CAPACITY_PORT_RULE: "capacity_id",
}

# Tables the capacity row points at, keyed by the column holding the reference.
REFERENCED_TABLES = {
    "locality_id": TableNames.LOCALITY,
    "resource_quota_id": TableNames.CAPACITY_RESOURCE_QUOTA,
}

# Which node types SAT Builder should instantiate. The totals node is always
# requested and is omitted automatically when the payload has no quota data.
RESOURCE_TYPE_TO_NODE_TYPE = {
    "cloud": "CloudCapacity",
    "edge": "EdgeCapacity",
}
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
    """Pick the node type from the capacity's resource type."""
    resource_type = (capacity.get("resource_type") or "").strip().lower()
    node_type = RESOURCE_TYPE_TO_NODE_TYPE.get(resource_type)
    if not node_type:
        supported = ", ".join(sorted(RESOURCE_TYPE_TO_NODE_TYPE))
        raise ValueError(
            f"Capacity has resource type '{capacity.get('resource_type')}', "
            f"which has no TOSCA node type. Expected one of: {supported}."
        )
    return [node_type, TOTALS_NODE_TYPE]


def generate_cdt_yaml(capacity_id: int) -> str:
    """Build the Capacity Description Template for a capacity."""
    payload = build_capacity_payload(capacity_id)
    params = {
        "node_types": node_types_for(payload[TableNames.CAPACITY_NEW.value]),
        "response_type": "yaml",
    }
    return generate_sat(payload, params, "capacity/build")
