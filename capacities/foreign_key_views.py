from .view_helpers import (
    CapacitySubtypeFieldsMixin,
    CloudCapacityViewMixin,
    EdgeCapacityViewMixin,
)

from editor.foreign_key_editor_views import (
    NewOneToManyForeignKeyResourceEditorView,
    NewOneToOneForeignKeyResourceEditorView,
    OneToManyForeignKeyResourceEditorView,
    OneToOneForeignKeyResourceEditorView,
)
from editor.foreign_key_views import (
    NonDialogBasedOneToManyFieldEditorSectionView,
    NonDialogBasedOneToOneFieldEditorSectionView,
    OneToManyFieldEditorSectionView,
    OneToOneFieldEditorSectionView,
)
from postgrest.table_names import TableNames


# Cloud Capacity views
class CloudCapacityOneToOneFieldEditorSectionView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, OneToOneFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    new_one_to_one_relation_reverse_base = "capacities:new_cloud_capacity_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "capacities:update_cloud_capacity_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "capacities:delete_cloud_capacity_one_to_one_relation"


class CloudCapacityOneToManyFieldEditorSectionView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, OneToManyFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_one_to_many_relation_reverse_base = "capacities:new_cloud_capacity_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "capacities:update_cloud_capacity_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "capacities:delete_cloud_capacity_one_to_many_relation"


class CloudCapacityNonDialogBasedOneToOneFieldView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, NonDialogBasedOneToOneFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_foreign_key_resource_editor_reverse_base = "capacities:cloud_capacity_new_one_to_one_foreign_key_resource_editor"
    foreign_key_resource_update_editor_reverse_base = "capacities:cloud_capacity_one_to_one_foreign_key_resource_update_editor"


class CloudCapacityNonDialogBasedOneToManyFieldView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, NonDialogBasedOneToManyFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_foreign_key_resource_editor_reverse_base = "capacities:cloud_capacity_new_one_to_many_foreign_key_resource_editor"
    foreign_key_resource_update_editor_reverse_base = "capacities:cloud_capacity_one_to_many_foreign_key_resource_update_editor"


class CloudCapacityNewOneToOneForeignKeyResourceEditorView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, NewOneToOneForeignKeyResourceEditorView):
    template_name = "capacities/cloud_capacity_new_one_to_one_fk_resource_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:cloud_capacity_editor"


class CloudCapacityOneToOneForeignKeyResourceEditorView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, OneToOneForeignKeyResourceEditorView):
    template_name = "capacities/cloud_capacity_one_to_one_fk_resource_update_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:cloud_capacity_editor"


class CloudCapacityNewOneToManyForeignKeyResourceEditorView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, NewOneToManyForeignKeyResourceEditorView):
    template_name = "capacities/cloud_capacity_new_one_to_many_fk_resource_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:cloud_capacity_editor"


class CloudCapacityOneToManyForeignKeyResourceEditorView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, OneToManyForeignKeyResourceEditorView):
    template_name = "capacities/cloud_capacity_one_to_many_fk_resource_update_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:cloud_capacity_editor"


# Edge Capacity views
class EdgeCapacityOneToOneFieldEditorSectionView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, OneToOneFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    new_one_to_one_relation_reverse_base = "capacities:new_edge_capacity_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "capacities:update_edge_capacity_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "capacities:delete_edge_capacity_one_to_one_relation"


class EdgeCapacityOneToManyFieldEditorSectionView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, OneToManyFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_one_to_many_relation_reverse_base = "capacities:new_edge_capacity_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "capacities:update_edge_capacity_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "capacities:delete_edge_capacity_one_to_many_relation"


class EdgeCapacityNonDialogBasedOneToOneFieldView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, NonDialogBasedOneToOneFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_foreign_key_resource_editor_reverse_base = "capacities:edge_capacity_new_one_to_one_foreign_key_resource_editor"
    foreign_key_resource_update_editor_reverse_base = "capacities:edge_capacity_one_to_one_foreign_key_resource_update_editor"


class EdgeCapacityNonDialogBasedOneToManyFieldView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, NonDialogBasedOneToManyFieldEditorSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_foreign_key_resource_editor_reverse_base = "capacities:edge_capacity_new_one_to_many_foreign_key_resource_editor"
    foreign_key_resource_update_editor_reverse_base = "capacities:edge_capacity_one_to_many_foreign_key_resource_update_editor"


class EdgeCapacityNewOneToOneForeignKeyResourceEditorView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, NewOneToOneForeignKeyResourceEditorView):
    template_name = "capacities/edge_capacity_new_one_to_one_fk_resource_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:edge_capacity_editor"


class EdgeCapacityOneToOneForeignKeyResourceEditorView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, OneToOneForeignKeyResourceEditorView):
    template_name = "capacities/edge_capacity_one_to_one_fk_resource_update_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:edge_capacity_editor"


class EdgeCapacityNewOneToManyForeignKeyResourceEditorView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, NewOneToManyForeignKeyResourceEditorView):
    template_name = "capacities/edge_capacity_new_one_to_many_fk_resource_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:edge_capacity_editor"


class EdgeCapacityOneToManyForeignKeyResourceEditorView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, OneToManyForeignKeyResourceEditorView):
    template_name = "capacities/edge_capacity_one_to_many_fk_resource_update_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:edge_capacity_editor"