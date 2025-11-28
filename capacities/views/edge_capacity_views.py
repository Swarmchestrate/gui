from django.urls import reverse_lazy

# from capacities.api.edge_capacity_api_clients import (
#     EdgeCapacityApiClient,
#     EdgeCapacityColumnMetadataApiClient,
# )
from capacities.api.mocks.mock_edge_capacity_clients import (
    EdgeCapacityApiClient,
    EdgeCapacityColumnMetadataApiClient,
)
from capacities.forms.edge_capacity_forms import (
    EdgeCapacityEditorForm,
    EdgeCapacityRegistrationForm,
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
    MultipleEditorFormsetProcessFormView,
)
from resource_management.views import (
    MultiResourceDeletionFormView,
    ResourceListContextMixin,
    ResourceListFormView,
)

from .capacity_views import (
    CapacityCostAndLocalityEditorProcessFormView,
    CapacityEditorRouterView,
    CapacityEnergyEditorProcessFormView,
    CapacityMetadataEditorProcessFormView,
    CapacitySecurityTrustAndAccessEditorProcessFormView,
    CapacitySpecsEditorProcessFormView,
)
from .mixins.edge_capacity_mixins import (
    AccessibleSensorsFormsetEditorViewMixin,
    DevicesFormsetEditorViewMixin,
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
    editor_url_reverse_base = "capacities:edge_capacity_editor"
    editor_start_url_reverse_base = "capacities:new_edge_capacity"
    editor_overview_url_reverse_base = "capacities:edge_capacity_overview"
    column_metadata_api_client_class = EdgeCapacityColumnMetadataApiClient
    editor_resource_list_url_reverse = "capacities:edge_capacity_list"
    new_resource_reverse = "capacities:new_edge_capacity"
    resource_deletion_reverse = "capacities:delete_edge_capacities"
    resource_type_name_singular = "edge capacity"
    resource_type_name_plural = "edge capacities"


class EdgeCapacityEditorStartFormView(EdgeCapacityViewMixin, EditorStartFormView):
    template_name = "capacities/new_edge_capacity_start.html"
    form_class = EdgeCapacityRegistrationForm


class EdgeCapacityEditorProcessFormView(EdgeCapacityViewMixin, EditorProcessFormView):
    template_name = "capacities/edge_capacity_editor.html"
    main_form_class = EdgeCapacityEditorForm
    success_url = reverse_lazy("capacities:new_edge_capacity")


class EdgeCapacityMetadataEditorProcessFormView(
    EdgeCapacityEditorProcessFormView, CapacityMetadataEditorProcessFormView
):
    pass


class EdgeCapacityCostAndLocalityEditorProcessFormView(
    EdgeCapacityEditorProcessFormView, CapacityCostAndLocalityEditorProcessFormView
):
    pass


class EdgeCapacityEnergyEditorProcessFormView(
    EdgeCapacityEditorProcessFormView, CapacityEnergyEditorProcessFormView
):
    pass


class EdgeCapacitySpecificEditorProcessFormView(
    EdgeCapacityEditorProcessFormView,
    MultipleEditorFormsetProcessFormView,
    AccessibleSensorsFormsetEditorViewMixin,
    DevicesFormsetEditorViewMixin,
):
    def dispatch(self, request, *args, **kwargs):
        self.add_accessible_sensors_formset_metadata()
        self.add_devices_formset_metadata()
        return super().dispatch(request, *args, **kwargs)


class EdgeCapacitySecurityTrustAndAccessEditorProcessFormView(
    EdgeCapacityEditorProcessFormView,
    CapacitySecurityTrustAndAccessEditorProcessFormView,
):
    pass


class EdgeCapacitySpecsEditorProcessFormView(
    EdgeCapacityEditorProcessFormView, CapacitySpecsEditorProcessFormView
):
    pass


class EdgeCapacityEditorRouterView(EdgeCapacityViewMixin, CapacityEditorRouterView):
    editor_view_class = EdgeCapacityEditorProcessFormView
    metadata_editor_view_class = EdgeCapacityMetadataEditorProcessFormView
    cost_and_locality_editor_view_class = (
        EdgeCapacityCostAndLocalityEditorProcessFormView
    )
    energy_editor_view_class = EdgeCapacityEnergyEditorProcessFormView
    security_trust_and_access_editor_view_class = (
        EdgeCapacitySecurityTrustAndAccessEditorProcessFormView
    )
    specs_editor_view_class = EdgeCapacitySpecsEditorProcessFormView

    def route_to_view(self, request, *args, **kwargs):
        if self.category.lower() == "edge specific":
            return EdgeCapacitySpecificEditorProcessFormView.as_view()(
                request, *args, **kwargs
            )
        return super().route_to_view(request, *args, **kwargs)


class MultiEdgeCapacityDeletionFormView(
    EdgeCapacityViewMixin, MultiResourceDeletionFormView
):
    success_url = reverse_lazy("capacities:delete_edge_capacities")


class EdgeCapacityListFormView(EdgeCapacityViewMixin, ResourceListFormView):
    template_name = "capacities/edge_capacities.html"


class EdgeCapacityEditorOverviewTemplateView(
    EdgeCapacityViewMixin, EditorOverviewTemplateView
):
    template_name = "capacities/edge_capacity_overview.html"
