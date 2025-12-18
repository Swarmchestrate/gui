from django.urls import reverse_lazy

from capacities.forms.edge_capacity_forms import (
    EdgeCapacityEditorForm,
    EdgeCapacityRegistrationForm,
)
from capacities.utils import (
    edge_capacity_type_readable,
    edge_capacity_type_readable_plural,
)
from editor.base_views import (
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    EditorContextMixin,
    ResourceTypeNameContextMixin,
)
from editor.views import (
    EditorOverviewTemplateView,
    EditorProcessFormView,
    EditorStartFormView,
)
from postgrest.api_clients import (
    EdgeCapacityApiClient,
    EdgeCapacityColumnMetadataApiClient,
)

# from postgrest.mocks.mock_api_clients import (
#     MockEdgeCapacityApiClient as EdgeCapacityApiClient,
# )
# from postgrest.mocks.mock_api_clients import (
#     MockEdgeCapacityColumnMetadataApiClient as EdgeCapacityColumnMetadataApiClient,
# )
from resource_management.views import (
    MultiResourceDeletionFormView,
    ResourceDeletionFormView,
    ResourceListContextMixin,
    ResourceListFormView,
)


# Edge Capacity
class EdgeCapacityViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    EditorContextMixin,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = EdgeCapacityApiClient
    editor_reverse_base = "capacities:edge_capacity_editor"
    editor_start_reverse_base = "capacities:new_edge_capacity"
    editor_overview_reverse_base = "capacities:edge_capacity_overview"
    column_metadata_api_client_class = EdgeCapacityColumnMetadataApiClient
    resource_list_reverse = "capacities:edge_capacity_list"
    new_resource_reverse = "capacities:new_edge_capacity"
    resource_deletion_reverse = "capacities:delete_edge_capacity"
    multi_resource_deletion_reverse = "capacities:delete_edge_capacities"
    resource_type_readable = edge_capacity_type_readable()
    resource_type_readable_plural = edge_capacity_type_readable_plural()


class EdgeCapacityEditorStartFormView(EdgeCapacityViewMixin, EditorStartFormView):
    template_name = "capacities/new_edge_capacity_start.html"
    form_class = EdgeCapacityRegistrationForm


class EdgeCapacityEditorProcessFormView(EdgeCapacityViewMixin, EditorProcessFormView):
    template_name = "capacities/edge_capacity_editor.html"
    form_class = EdgeCapacityEditorForm
    success_url = reverse_lazy("capacities:new_edge_capacity")


class EdgeCapacityDeletionFormView(EdgeCapacityViewMixin, ResourceDeletionFormView):
    template_name = "capacities/edge_capacities.html"
    success_url = reverse_lazy("capacities:delete_cloud_capacities")


class MultiEdgeCapacityDeletionFormView(
    EdgeCapacityViewMixin, MultiResourceDeletionFormView
):
    template_name = "capacities/edge_capacities.html"
    success_url = reverse_lazy("capacities:delete_edge_capacities")


class EdgeCapacityListFormView(EdgeCapacityViewMixin, ResourceListFormView):
    template_name = "capacities/edge_capacities.html"


class EdgeCapacityEditorOverviewTemplateView(
    EdgeCapacityViewMixin, EditorOverviewTemplateView
):
    template_name = "capacities/edge_capacity_overview.html"
