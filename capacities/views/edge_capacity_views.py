from django.urls import reverse_lazy

from capacities.api.mocks.mock_edge_capacity_clients import (
    EdgeCapacityApiEndpoint,
    EdgeCapacityColumnMetadataApiEndpoint,
)

# from capacities.api.endpoints.edge_capacity import (
#     EdgeCapacityApiEndpoint,
#     EdgeCapacityColumnMetadataApiEndpoint,
# )
from capacities.forms.edge_capacity_forms import (
    EdgeCapacityEditorForm,
    EdgeCapacityRegistrationForm,
)
from editor.base_views import (
    EditorOverviewTemplateView,
    EditorProcessFormView,
    EditorStartFormView,
    EditorView,
    MultipleEditorFormsetProcessFormView,
    RegistrationsListFormView,
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
class EdgeCapacityEditorView(EditorView):
    editor_registration_list_url_reverse = "capacities:edge_capacities_list"
    editor_url_reverse_base = "capacities:edge_capacity_editor"
    editor_start_url_reverse_base = "capacities:new_edge_capacity"
    editor_overview_url_reverse_base = "capacities:edge_capacity_overview"
    registration_type_name_singular = "edge capacity"
    registration_type_name_plural = "edge capacities"
    title_base = "New Edge Capacity"
    api_endpoint_class = EdgeCapacityApiEndpoint
    column_metadata_api_endpoint_class = EdgeCapacityColumnMetadataApiEndpoint


class EdgeCapacityEditorStartFormView(EdgeCapacityEditorView, EditorStartFormView):
    template_name = "capacities/new_edge_capacity_start.html"
    form_class = EdgeCapacityRegistrationForm


class EdgeCapacityEditorProcessFormView(EdgeCapacityEditorView, EditorProcessFormView):
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


class EdgeCapacityEditorRouterView(EdgeCapacityEditorView, CapacityEditorRouterView):
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


class EdgeCapacityRegistrationsListFormView(
    EdgeCapacityEditorView, RegistrationsListFormView
):
    template_name = "capacities/edge_capacities.html"
    new_registration_reverse = "capacities:new_edge_capacity"


class EdgeCapacityEditorOverviewTemplateView(
    EdgeCapacityEditorView, EditorOverviewTemplateView
):
    template_name = "capacities/edge_capacity_overview.html"
