def capacity_type_readable() -> str:
    return "capacity"


def capacity_type_readable_plural() -> str:
    return "capacities"


def cloud_capacity_type_readable() -> str:
    return f"cloud {capacity_type_readable()}"


def cloud_capacity_type_readable_plural() -> str:
    return f"cloud {capacity_type_readable_plural()}"


def edge_capacity_type_readable() -> str:
    return f"edge {capacity_type_readable()}"


def edge_capacity_type_readable_plural() -> str:
    return f"edge {capacity_type_readable_plural()}"
