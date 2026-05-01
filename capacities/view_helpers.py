from dataclasses import dataclass


@dataclass
class CloudCapacityViewMixin:
    table_name = 'cloud_capacity'
    editor_reverse_base = "capacities:cloud_capacity_editor"
    editor_start_reverse_base = "capacities:new_cloud_capacity"
    editor_overview_reverse_base = "capacities:cloud_capacity_overview"
    resource_list_reverse = "capacities:cloud_capacity_list"
    new_resource_reverse = "capacities:new_cloud_capacity"
    resource_deletion_reverse = "capacities:delete_cloud_capacity"
    multi_resource_deletion_reverse = "capacities:delete_cloud_capacities"
    resource_type = "cloud_capacity"


@dataclass
class EdgeCapacityViewMixin:
    editor_reverse_base = "capacities:edge_capacity_editor"
    editor_start_reverse_base = "capacities:new_edge_capacity"
    editor_overview_reverse_base = "capacities:edge_capacity_overview"
    resource_list_reverse = "capacities:edge_capacity_list"
    new_resource_reverse = "capacities:new_edge_capacity"
    resource_deletion_reverse = "capacities:delete_edge_capacity"
    multi_resource_deletion_reverse = "capacities:delete_edge_capacities"
    resource_type = "edge_capacity"