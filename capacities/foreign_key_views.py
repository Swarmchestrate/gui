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
    UpdateOneToManyRelationFormView,
    UpdateOneToOneRelationFormView,
)


# Cloud Capacity views
class CloudCapacityNewOneToOneRelationFormView(CloudCapacityViewMixin, NewOneToOneRelationFormView):
    template_name = "capacities/cloud_capacity_editor.html"
    table_name = "capacity_new"

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
    table_name = "capacity_new"

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
    table_name = "capacity_new"

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
    table_name = "capacity_new"
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
    table_name = "capacity_new"
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
    table_name = "capacity_new"
    possible_fk_table_column_name = "capacity_id"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


# Edge Capacity views
class EdgeCapacityNewOneToOneRelationFormView(EdgeCapacityViewMixin, NewOneToOneRelationFormView):
    template_name = "capacities/edge_capacity_editor.html"
    table_name = "capacity_new"

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
    table_name = "capacity_new"

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
    table_name = "capacity_new"

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
    table_name = "capacity_new"
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
    table_name = "capacity_new"
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
    table_name = "capacity_new"
    possible_fk_table_column_name = "capacity_id"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:edge_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)