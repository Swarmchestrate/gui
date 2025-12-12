from dataclasses import dataclass

from django.urls import reverse_lazy
from django.views.generic import FormView

from capacities.forms.cloud_capacity_forms import (
    CloudCapacityEditorForm,
    CloudCapacityRegistrationForm,
)
from capacities.utils import (
    cloud_capacity_type_readable,
    cloud_capacity_type_readable_plural,
)
from editor.base_views import (
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    EditorContextMixin,
    ResourceTypeNameContextMixin,
)
from editor.views import (
    DeleteOneToManyRelationFormView,
    DeleteOneToOneRelationFormView,
    EditorOverviewTemplateView,
    EditorProcessFormView,
    EditorStartFormView,
    NewOneToManyRelationFormView,
    NewOneToOneRelationFormView,
    UpdateOneToManyRelationFormView,
    UpdateOneToOneRelationFormView,
)

# from postgrest.api_clients import (
#     CloudCapacityApiClient,
#     ColumnMetadataApiClient,
# )
from postgrest.mocks.mock_api_clients import (
    CloudCapacityApiClient,
    CloudCapacityColumnMetadataApiClient,
)
from resource_management.views import (
    MultiResourceDeletionFormView,
    ResourceDeletionFormView,
    ResourceListContextMixin,
    ResourceListFormView,
)


# Cloud Capacity
@dataclass
class CloudCapacityViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    EditorContextMixin,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = CloudCapacityApiClient
    editor_reverse_base = "capacities:cloud_capacity_editor"
    editor_start_reverse_base = "capacities:new_cloud_capacity"
    editor_overview_reverse_base = "capacities:cloud_capacity_overview"
    column_metadata_api_client_class = CloudCapacityColumnMetadataApiClient
    resource_list_reverse = "capacities:cloud_capacity_list"
    new_resource_reverse = "capacities:new_cloud_capacity"
    resource_deletion_reverse = "capacities:delete_cloud_capacity"
    multi_resource_deletion_reverse = "capacities:delete_cloud_capacities"
    resource_type_readable = cloud_capacity_type_readable()
    resource_type_readable_plural = cloud_capacity_type_readable_plural()


class CloudCapacityEditorStartFormView(
    CloudCapacityViewMixin, EditorStartFormView, FormView
):
    template_name = "capacities/new_cloud_capacity_start.html"
    form_class = CloudCapacityRegistrationForm


class CloudCapacityEditorProcessFormView(CloudCapacityViewMixin, EditorProcessFormView):
    template_name = "capacities/cloud_capacity_editor.html"
    form_class = CloudCapacityEditorForm
    success_url = reverse_lazy("capacities:new_cloud_capacity")
    new_one_to_one_relation_reverse_base = (
        "capacities:new_cloud_capacity_one_to_one_relation"
    )
    update_one_to_one_relation_reverse_base = (
        "capacities:update_cloud_capacity_one_to_one_relation"
    )
    delete_one_to_one_relation_reverse_base = (
        "capacities:delete_cloud_capacity_one_to_one_relation"
    )
    new_one_to_many_relation_reverse_base = (
        "capacities:new_cloud_capacity_one_to_many_relation"
    )
    update_one_to_many_relation_reverse_base = (
        "capacities:update_cloud_capacity_one_to_many_relation"
    )
    delete_one_to_many_relation_reverse_base = (
        "capacities:delete_cloud_capacity_one_to_many_relation"
    )


class CloudCapacityDeletionFormView(CloudCapacityViewMixin, ResourceDeletionFormView):
    template_name = "capacities/cloud_capacities.html"
    success_url = reverse_lazy("capacities:delete_cloud_capacities")


class MultiCloudCapacityDeletionFormView(
    CloudCapacityViewMixin, MultiResourceDeletionFormView
):
    template_name = "capacities/cloud_capacities.html"
    success_url = reverse_lazy("capacities:delete_cloud_capacities")


class CloudCapacityListFormView(CloudCapacityViewMixin, ResourceListFormView):
    template_name = "capacities/cloud_capacities.html"


class CloudCapacityEditorOverviewTemplateView(
    CloudCapacityViewMixin, EditorOverviewTemplateView
):
    template_name = "capacities/cloud_capacity_overview.html"


class CloudCapacityNewOneToOneRelationFormView(
    CloudCapacityViewMixin, NewOneToOneRelationFormView
):
    template_name = "capacities/cloud_capacity_editor.html"
    api_client = CloudCapacityApiClient

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityUpdateOneToOneRelationFormView(
    CloudCapacityViewMixin, UpdateOneToOneRelationFormView
):
    template_name = "capacities/cloud_capacity_editor.html"
    api_client = CloudCapacityApiClient

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityDeleteOneToOneRelationFormView(
    CloudCapacityViewMixin, DeleteOneToOneRelationFormView
):
    template_name = "capacities/cloud_capacity_editor.html"
    api_client = CloudCapacityApiClient

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityNewOneToManyRelationFormView(
    CloudCapacityViewMixin, NewOneToManyRelationFormView
):
    template_name = "capacities/cloud_capacity_editor.html"
    api_client = CloudCapacityApiClient

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityUpdateOneToManyRelationFormView(
    CloudCapacityViewMixin, UpdateOneToManyRelationFormView
):
    template_name = "capacities/cloud_capacity_editor.html"
    api_client = CloudCapacityApiClient

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class CloudCapacityDeleteOneToManyRelationFormView(
    CloudCapacityViewMixin, DeleteOneToManyRelationFormView
):
    template_name = "capacities/cloud_capacity_editor.html"
    api_client = CloudCapacityApiClient

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "capacities:cloud_capacity_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)
