def humanise_resource_type(resource_type):
    resource_types_humanised = {
        "application": "application",
        "application_new": "application",
        "application_pref_resource_provider": "preferred resource provider",
        "application_behaviour": "behaviour",
        "application_volume": "volume",
        "application_colocate": "colocation",
        "application_environment_var": "environment variable",
        "application_security_rule": "security rule",
        "capacity": "capacity",
        "capacity_new": "capacity",
        "capacity_operating_system": "operating system",
        "capacity_instance_type": "instance type",
        "capacity_resource_quota": "resource quota",
        "capacity_energy_consumption": "energy consumption",
        "capacity_price": "price",
        "cloud_capacity": "cloud capacity",
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
        "application_security_rule": "security rules",
        "capacity": "capacities",
        "capacity_new": "capacities",
        "capacity_operating_system": "operating systems",
        "capacity_instance_type": "instance types",
        "capacity_resource_quota": "resource quotas",
        "capacity_energy_consumption": "energy consumptions",
        "capacity_price": "prices",
        "cloud_capacity": "cloud capacities",
        "edge_capacity": "edge capacities",
        "locality": "localities",
    }
    return resource_types_humanised.get(
        resource_type,
        f"{' '.join(resource_type.split('_'))} registrations"
    )