from dataclasses import dataclass


# Cloud and edge capacities share the capacity_new table, but each is a distinct
# TOSCA node type with its own properties. A capacity is one subtype, so the
# others' properties are hidden rather than shown empty.
# Keyed by the value of capacity_new.cloud, or "edge" for edge capacities.
# Covers capacity_new and capacity_instance_type: a flavour names its instance
# differently per platform, and an edge capacity names it at all.
SUBTYPE_ONLY_PROPERTIES = {
    "edge": [
        "edge_ip",
        "edge_local_ip",
        "credentials",
        "ssh_auth_method",
        "ssh_port",
        "ssh_user",
    ],
    "aws": [
        "instance_type",   # capacity_instance_type, e.g. t3.micro
    ],
    "openstack": [
        "network_id",
        "project_id",
        "use_block_device",
        "flavor_name",     # capacity_instance_type, e.g. m2.medium
    ],
}

# Declared by both cloud subtypes but not by EdgeCapacity.
CLOUD_ONLY_PROPERTIES = [
    "security_group",
    "security_groups",
    "ssh_key_name",
    "os_uuid",
]

# Set when the capacity is created and not editable afterwards.
FIXED_AT_CREATION = [
    "resource_type",
    "cloud",
]

# Identifiers the system owns. Nothing in the profile binds them, and a user
# has no way to know a correct value, so they are never offered on a form.
SYSTEM_MANAGED = [
    "instance_type_uuid",
]


def subtype_of(capacity: dict) -> str | None:
    """Which set of properties a capacity uses: 'edge', 'aws' or 'openstack'."""
    if (capacity.get("resource_type") or "").strip().lower() == "edge":
        return "edge"
    cloud = (capacity.get("cloud") or "").strip().lower()
    return cloud or None


def hidden_capacity_properties(capacity: dict) -> list[str]:
    """Properties belonging to a subtype other than this capacity's."""
    subtype = subtype_of(capacity)
    if subtype not in SUBTYPE_ONLY_PROPERTIES:
        # Unknown subtype: hide nothing rather than guess.
        return []

    hidden = [
        name
        for other, names in SUBTYPE_ONLY_PROPERTIES.items()
        if other != subtype
        for name in names
    ]
    if subtype == "edge":
        hidden.extend(CLOUD_ONLY_PROPERTIES)
    return hidden


class CapacitySubtypeFieldsMixin:
    """Restricts the form to the properties of the capacity's own subtype."""

    # Nullable because each platform names its instance differently, but a
    # flavour is not usable without one. The subtype filter hides whichever
    # does not apply.
    extra_new_fields = ["instance_type", "flavor_name", "os_uuid"]

    @property
    def disabled_properties(self) -> list[str]:
        resource = getattr(self, "resource", None)
        capacity = resource.as_dict() if resource is not None else {}
        return [*FIXED_AT_CREATION, *SYSTEM_MANAGED, *hidden_capacity_properties(capacity)]


@dataclass
class CloudCapacityViewMixin:
    # No table_name default: views set their own, and a missing one should fail
    # loudly rather than silently querying a table that does not exist.
    editor_reverse_base = "capacities:cloud_capacity_editor"
    editor_one_to_one_section_reverse_base = "capacities:cloud_capacity_editor_one_to_one_section"
    editor_one_to_many_section_reverse_base = "capacities:cloud_capacity_editor_one_to_many_section"
    editor_non_dialog_based_one_to_one_section_reverse_base = "capacities:cloud_capacity_editor_non_dialog_based_one_to_one_section"
    editor_non_dialog_based_one_to_many_section_reverse_base = "capacities:cloud_capacity_editor_non_dialog_based_one_to_many_section"
    editor_start_reverse_base = "capacities:new_cloud_capacity"
    editor_overview_reverse_base = "capacities:cloud_capacity_overview"
    resource_list_reverse = "capacities:cloud_capacity_list"
    new_resource_reverse = "capacities:new_cloud_capacity"
    resource_deletion_reverse = "capacities:delete_cloud_capacity"
    multi_resource_deletion_reverse = "capacities:delete_cloud_capacities"
    tosca_template_download_reverse_base = "capacities:cloud_cdt_download"
    resource_type = "cloud_capacity"


@dataclass
class EdgeCapacityViewMixin:
    editor_reverse_base = "capacities:edge_capacity_editor"
    editor_one_to_one_section_reverse_base = "capacities:edge_capacity_editor_one_to_one_section"
    editor_one_to_many_section_reverse_base = "capacities:edge_capacity_editor_one_to_many_section"
    editor_non_dialog_based_one_to_one_section_reverse_base = "capacities:edge_capacity_editor_non_dialog_based_one_to_one_section"
    editor_non_dialog_based_one_to_many_section_reverse_base = "capacities:edge_capacity_editor_non_dialog_based_one_to_many_section"
    editor_start_reverse_base = "capacities:new_edge_capacity"
    editor_overview_reverse_base = "capacities:edge_capacity_overview"
    resource_list_reverse = "capacities:edge_capacity_list"
    new_resource_reverse = "capacities:new_edge_capacity"
    resource_deletion_reverse = "capacities:delete_edge_capacity"
    multi_resource_deletion_reverse = "capacities:delete_edge_capacities"
    tosca_template_download_reverse_base = "capacities:edge_cdt_download"
    resource_type = "edge_capacity"