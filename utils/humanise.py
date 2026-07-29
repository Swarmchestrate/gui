# Columns that name a row, in the order they are worth trying. A row is shown
# by whichever it has, because "mymedium" tells a provider what they are looking
# at and "Instance Flavour 472246" does not.
NAMING_COLUMNS = ("name", "property_name", "target")


def resource_label(resource, resource_type, resource_id):
    """Label a row the way the person who created it would recognise it.

    Falls back to the type and id, so a row with nothing to name it by is still
    identifiable rather than blank.
    """
    for column in NAMING_COLUMNS:
        value = (resource or {}).get(column)
        if value is not None and str(value).strip():
            return str(value).strip()
    return f"{humanise_resource_type(resource_type).title()} {resource_id}"


def humanise_resource_type(resource_type):
    resource_types_humanised = {
        "application": "application",
        "application_new": "application",
        "application_pref_resource_provider": "preferred resource provider",
        "application_behaviour": "behaviour",
        "application_volume": "volume",
        "application_colocate": "colocation",
        "application_environment_var": "environment variable",
        "application_microservice": "microservice",
        # Named for what a user is doing, not for the TOSCA construct behind it.
        "application_node_filter": "resource requirement",
        "application_property": "additional Kubernetes property",
        "application_security_rule": "security rule",
        "capacity": "capacity",
        "capacity_new": "capacity",
        "capacity_operating_system": "operating system",
        "capacity_instance_type": "instance flavour",
        "capacity_resource_quota": "resource quota",
        "capacity_energy_consumption": "energy consumption",
        "capacity_price": "price",
        "cloud_capacity": "cloud capacity",
        "column_metadata": "column metadata",
        "edge_capacity": "edge capacity",
        "locality": "locality",
    }
    return resource_types_humanised.get(
        resource_type,
        f"{' '.join(resource_type.split('_'))}"
    )


def humanise_resource_type_plural(resource_type):
    resource_types_humanised = {
        "application": "applications",
        "application_new": "applications",
        "application_pref_resource_provider": "preferred resource providers",
        "application_behaviour": "behaviours",
        "application_volume": "volumes",
        "application_colocate": "colocations",
        "application_environment_var": "environment variables",
        "application_microservice": "microservices",
        "application_node_filter": "resource requirements",
        "application_property": "additional Kubernetes properties",
        "application_security_rule": "security rules",
        "capacity": "capacities",
        "capacity_new": "capacities",
        "capacity_operating_system": "operating systems",
        "capacity_instance_type": "instance flavours",
        "capacity_resource_quota": "resource quotas",
        "capacity_energy_consumption": "energy consumptions",
        "capacity_price": "prices",
        "cloud_capacity": "cloud capacities",
        "column_metadata": "column metadata",
        "edge_capacity": "edge capacities",
        "locality": "localities",
    }
    return resource_types_humanised.get(
        resource_type,
        f"{' '.join(resource_type.split('_'))} registrations"
    )

def humanise_enum_value(value):
    """Label an enum value for display.

    Stored values follow the TOSCA profile - a capacity's cloud is 'aws' or
    'openstack' because that is what ends up in the generated template - but
    those are not what a provider recognises in a dropdown.
    """
    enum_values_humanised = {
        "aws": "Amazon EC2",
        "openstack": "OpenStack Nova",
    }
    return enum_values_humanised.get(
        value,
        f"{' '.join(str(value).split('_'))}"
    )
