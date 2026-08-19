from .view_helpers import (
    CapacitySubtypeFieldsMixin,
    CloudCapacityViewMixin,
    EdgeCapacityViewMixin,
)

from editor.foreign_key_editor_views import (
    NewOneToManyForeignKeyEditorView,
    NewOneToOneForeignKeyEditorView,
    OneToManyForeignKeyEditorView,
    OneToOneForeignKeyEditorView,
)
from editor.foreign_key_views import (
    OneToManyFieldSectionView,
    OneToOneFieldSectionView,
    OneToManyFieldPopupSectionView,
    OneToOneFieldPopupSectionView,
)
from postgrest.table_names import TableNames


# Cloud Capacity views
class CloudCapacityOneToOneFieldPopupSectionView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, OneToOneFieldPopupSectionView):
    table_name = TableNames.CAPACITY_NEW
    new_one_to_one_relation_reverse_base = "capacities:new_cloud_capacity_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "capacities:update_cloud_capacity_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "capacities:delete_cloud_capacity_one_to_one_relation"


class CloudCapacityOneToManyFieldPopupSectionView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, OneToManyFieldPopupSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_one_to_many_relation_reverse_base = "capacities:new_cloud_capacity_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "capacities:update_cloud_capacity_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "capacities:delete_cloud_capacity_one_to_many_relation"


class CloudCapacityOneToOneFieldSectionView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, OneToOneFieldSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_foreign_key_editor_reverse_base = "capacities:cloud_capacity_new_one_to_one_foreign_key_editor"
    foreign_key_update_editor_reverse_base = "capacities:cloud_capacity_one_to_one_foreign_key_update_editor"


class CloudCapacityOneToManyFieldSectionView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, OneToManyFieldSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_foreign_key_editor_reverse_base = "capacities:cloud_capacity_new_one_to_many_foreign_key_editor"
    foreign_key_update_editor_reverse_base = "capacities:cloud_capacity_one_to_many_foreign_key_update_editor"


class CloudCapacityNewOneToOneForeignKeyEditorView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, NewOneToOneForeignKeyEditorView):
    template_name = "capacities/cloud_capacity_new_one_to_one_fk_resource_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:cloud_capacity_editor"


class CloudCapacityOneToOneForeignKeyEditorView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, OneToOneForeignKeyEditorView):
    template_name = "capacities/cloud_capacity_one_to_one_fk_resource_update_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:cloud_capacity_editor"


class CloudCapacityNewOneToManyForeignKeyEditorView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, NewOneToManyForeignKeyEditorView):
    template_name = "capacities/cloud_capacity_new_one_to_many_fk_resource_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:cloud_capacity_editor"


class CloudCapacityOneToManyForeignKeyEditorView(CapacitySubtypeFieldsMixin, CloudCapacityViewMixin, OneToManyForeignKeyEditorView):
    template_name = "capacities/cloud_capacity_one_to_many_fk_resource_update_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:cloud_capacity_editor"


# Edge Capacity views
class EdgeCapacityOneToOneFieldPopupSectionView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, OneToOneFieldPopupSectionView):
    table_name = TableNames.CAPACITY_NEW
    new_one_to_one_relation_reverse_base = "capacities:new_edge_capacity_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "capacities:update_edge_capacity_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "capacities:delete_edge_capacity_one_to_one_relation"


class EdgeCapacityOneToManyFieldPopupSectionView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, OneToManyFieldPopupSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_one_to_many_relation_reverse_base = "capacities:new_edge_capacity_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "capacities:update_edge_capacity_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "capacities:delete_edge_capacity_one_to_many_relation"


class EdgeCapacityOneToOneFieldSectionView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, OneToOneFieldSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_foreign_key_editor_reverse_base = "capacities:edge_capacity_new_one_to_one_foreign_key_editor"
    foreign_key_update_editor_reverse_base = "capacities:edge_capacity_one_to_one_foreign_key_update_editor"


class EdgeCapacityOneToManyFieldSectionView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, OneToManyFieldSectionView):
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"
    new_foreign_key_editor_reverse_base = "capacities:edge_capacity_new_one_to_many_foreign_key_editor"
    foreign_key_update_editor_reverse_base = "capacities:edge_capacity_one_to_many_foreign_key_update_editor"


class EdgeCapacityNewOneToOneForeignKeyEditorView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, NewOneToOneForeignKeyEditorView):
    template_name = "capacities/edge_capacity_new_one_to_one_fk_resource_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:edge_capacity_editor"


class EdgeCapacityOneToOneForeignKeyEditorView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, OneToOneForeignKeyEditorView):
    template_name = "capacities/edge_capacity_one_to_one_fk_resource_update_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:edge_capacity_editor"


class EdgeCapacityNewOneToManyForeignKeyEditorView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, NewOneToManyForeignKeyEditorView):
    template_name = "capacities/edge_capacity_new_one_to_many_fk_resource_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:edge_capacity_editor"


class EdgeCapacityOneToManyForeignKeyEditorView(CapacitySubtypeFieldsMixin, EdgeCapacityViewMixin, OneToManyForeignKeyEditorView):
    template_name = "capacities/edge_capacity_one_to_many_fk_resource_update_editor.html"
    table_name = TableNames.CAPACITY_NEW
    column_metadata_table_name = TableNames.CAPACITY
    success_reverse_base = "capacities:edge_capacity_editor"