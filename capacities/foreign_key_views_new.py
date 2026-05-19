from .view_helpers import CloudCapacityViewMixin

from editor.foreign_key_views_new import (
    DialogBasedOneToManyFieldView,
    DialogBasedOneToOneFieldView,
    EditorBasedOneToManyFieldView,
    EditorBasedOneToOneFieldView,
    EditorForeignKeyFieldView,
)
from postgrest.table_names import TableNames

class CloudCapacityDialogBasedOneToOneFieldView(CloudCapacityViewMixin, DialogBasedOneToOneFieldView):
    table_name = TableNames.CAPACITY_NEW
    new_one_to_one_relation_reverse_base = "capacities:new_cloud_capacity_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "capacities:update_cloud_capacity_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "capacities:delete_cloud_capacity_one_to_one_relation"


class CloudCapacityDialogBasedOneToManyFieldView(CloudCapacityViewMixin, DialogBasedOneToManyFieldView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_one_to_many_relation_reverse_base = "capacities:new_cloud_capacity_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "capacities:update_cloud_capacity_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "capacities:delete_cloud_capacity_one_to_many_relation"


class CloudCapacityEditorBasedOneToOneFieldView(CloudCapacityViewMixin, EditorBasedOneToOneFieldView):
    view_class = CloudCapacityDialogBasedOneToOneFieldView
    table_name = TableNames.CAPACITY_NEW
    new_one_to_one_relation_reverse_base = "capacities:new_cloud_capacity_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "capacities:update_cloud_capacity_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "capacities:delete_cloud_capacity_one_to_one_relation"


class CloudCapacityEditorBasedOneToManyFieldView(CloudCapacityViewMixin, EditorBasedOneToManyFieldView):
    view_class = CloudCapacityDialogBasedOneToManyFieldView
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_one_to_many_relation_reverse_base = "capacities:new_cloud_capacity_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "capacities:update_cloud_capacity_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "capacities:delete_cloud_capacity_one_to_many_relation"


class CloudCapacityEditorForeignKeyFieldView(
        CloudCapacityViewMixin,
        EditorForeignKeyFieldView):
    table_name = TableNames.CAPACITY_NEW
    dialog_based_one_to_one_field_view_class = CloudCapacityDialogBasedOneToOneFieldView
    dialog_based_one_to_many_field_view_class = CloudCapacityDialogBasedOneToManyFieldView
    editor_based_one_to_one_field_view_class = CloudCapacityEditorBasedOneToOneFieldView
    editor_based_one_to_many_field_view_class = CloudCapacityEditorBasedOneToManyFieldView