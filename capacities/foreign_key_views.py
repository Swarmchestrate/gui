from django.urls import reverse_lazy

from .view_helpers import (
    CloudCapacityViewMixin,
    EdgeCapacityViewMixin,
)

from editor.foreign_key_views import (
    DeleteOneToManyRelationFormView,
    DeleteOneToOneRelationFormView,
    NewOneToManyRelationFormView,
    NewOneToOneRelationFormView,
    OneToManyFieldEditorSectionView,
    OneToOneFieldEditorSectionView,
    UpdateOneToManyRelationFormView,
    UpdateOneToOneRelationFormView,
)
from postgrest.table_names import TableNames


# Cloud Capacity views
class CloudCapacityNewOneToOneRelationFormView(CloudCapacityViewMixin, NewOneToOneRelationFormView):
    template_name = "capacities/cloud_capacity_editor.html"
    table_name = TableNames.CAPACITY_NEW

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityUpdateOneToOneRelationFormView(
        CloudCapacityViewMixin,
        UpdateOneToOneRelationFormView):
    template_name = "capacities/cloud_capacity_editor.html"
    table_name = TableNames.CAPACITY_NEW

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityDeleteOneToOneRelationFormView(
        CloudCapacityViewMixin,
        DeleteOneToOneRelationFormView):
    template_name = "capacities/cloud_capacity_editor.html"
    table_name = TableNames.CAPACITY_NEW

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityNewOneToManyRelationFormView(
        CloudCapacityViewMixin,
        NewOneToManyRelationFormView):
    template_name = "capacities/cloud_capacity_editor.html"
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityUpdateOneToManyRelationFormView(
        CloudCapacityViewMixin,
        UpdateOneToManyRelationFormView):
    template_name = "capacities/cloud_capacity_editor.html"
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityDeleteOneToManyRelationFormView(
        CloudCapacityViewMixin,
        DeleteOneToManyRelationFormView):
    template_name = "capacities/cloud_capacity_editor.html"
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


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


# Edge Capacity views
class EdgeCapacityNewOneToOneRelationFormView(EdgeCapacityViewMixin, NewOneToOneRelationFormView):
    template_name = "capacities/edge_capacity_editor.html"
    table_name = TableNames.CAPACITY_NEW

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:edge_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class EdgeCapacityUpdateOneToOneRelationFormView(
        EdgeCapacityViewMixin,
        UpdateOneToOneRelationFormView):
    template_name = "capacities/edge_capacity_editor.html"
    table_name = TableNames.CAPACITY_NEW

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:edge_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class EdgeCapacityDeleteOneToOneRelationFormView(
        EdgeCapacityViewMixin,
        DeleteOneToOneRelationFormView):
    template_name = "capacities/edge_capacity_editor.html"
    table_name = TableNames.CAPACITY_NEW

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:edge_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class EdgeCapacityNewOneToManyRelationFormView(
        EdgeCapacityViewMixin,
        NewOneToManyRelationFormView):
    template_name = "capacities/edge_capacity_editor.html"
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:edge_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class EdgeCapacityUpdateOneToManyRelationFormView(
        EdgeCapacityViewMixin,
        UpdateOneToManyRelationFormView):
    template_name = "capacities/edge_capacity_editor.html"
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:edge_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class EdgeCapacityDeleteOneToManyRelationFormView(
        EdgeCapacityViewMixin,
        DeleteOneToManyRelationFormView):
    template_name = "capacities/edge_capacity_editor.html"
    table_name = TableNames.CAPACITY_NEW
    possible_fk_table_column_name = "capacity_id"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:edge_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


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