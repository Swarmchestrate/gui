from django.urls import reverse_lazy

from .view_helpers import (
    CloudCapacityViewMixin,
    EdgeCapacityViewMixin,
)

from editor.foreign_key_views import (
    NonDialogBasedOneToManyFieldEditorSectionView,
    NonDialogBasedOneToOneFieldEditorSectionView,
    OneToManyFieldEditorSectionView,
    OneToOneFieldEditorSectionView,
)
from postgrest.table_names import TableNames


# Cloud Capacity views
class CloudCapacityOneToOneFieldEditorSectionView(CloudCapacityViewMixin, OneToOneFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    new_one_to_one_relation_reverse_base = "capacities:new_cloud_capacity_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "capacities:update_cloud_capacity_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "capacities:delete_cloud_capacity_one_to_one_relation"


class CloudCapacityOneToManyFieldEditorSectionView(CloudCapacityViewMixin, OneToManyFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_one_to_many_relation_reverse_base = "capacities:new_cloud_capacity_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "capacities:update_cloud_capacity_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "capacities:delete_cloud_capacity_one_to_many_relation"


class CloudCapacityNonDialogBasedOneToOneFieldView(CloudCapacityViewMixin, NonDialogBasedOneToOneFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_foreign_key_resource_editor_reverse_base = "capacities:cloud_capacity_new_foreign_key_resource_editor"
    foreign_key_resource_update_editor_reverse_base = "capacities:cloud_capacity_foreign_key_resource_update_editor"


class CloudCapacityNonDialogBasedOneToManyFieldView(CloudCapacityViewMixin, NonDialogBasedOneToManyFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_foreign_key_resource_editor_reverse_base = "capacities:cloud_capacity_new_foreign_key_resource_editor"
    foreign_key_resource_update_editor_reverse_base = "capacities:cloud_capacity_foreign_key_resource_update_editor"


# Edge Capacity views
class EdgeCapacityOneToOneFieldEditorSectionView(EdgeCapacityViewMixin, OneToOneFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    new_one_to_one_relation_reverse_base = "capacities:new_edge_capacity_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "capacities:update_edge_capacity_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "capacities:delete_edge_capacity_one_to_one_relation"


class EdgeCapacityOneToManyFieldEditorSectionView(EdgeCapacityViewMixin, OneToManyFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_one_to_many_relation_reverse_base = "capacities:new_edge_capacity_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "capacities:update_edge_capacity_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "capacities:delete_edge_capacity_one_to_many_relation"


class EdgeCapacityNonDialogBasedOneToOneFieldView(EdgeCapacityViewMixin, NonDialogBasedOneToOneFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_foreign_key_resource_editor_reverse_base = "capacities:edge_capacity_new_foreign_key_resource_editor"
    foreign_key_resource_update_editor_reverse_base = "capacities:edge_capacity_foreign_key_resource_update_editor"


class EdgeCapacityNonDialogBasedOneToManyFieldView(EdgeCapacityViewMixin, NonDialogBasedOneToManyFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_foreign_key_resource_editor_reverse_base = "capacities:edge_capacity_new_foreign_key_resource_editor"
    foreign_key_resource_update_editor_reverse_base = "capacities:edge_capacity_foreign_key_resource_update_editor"