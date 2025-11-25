from django.urls import reverse_lazy
from django.views.generic import FormView

# from capacities.api.cloud_capacity_api_clients import (
#     CloudCapacityApiClient,
#     CloudCapacityColumnMetadataApiClient,
# )
from capacities.api.mocks.mock_cloud_capacity_clients import (
    CloudCapacityApiClient,
    CloudCapacityColumnMetadataApiClient,
)
from capacities.forms.cloud_capacity_forms import (
    CloudCapacityEditorForm,
    CloudCapacityRegistrationForm,
)
from editor.base_views import (
    EditorOverviewTemplateView,
    EditorProcessFormView,
    EditorStartFormView,
    EditorView,
    MultipleEditorFormsetProcessFormView,
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
from .mixins.cloud_capacity_mixins import (
    ArchitectureFormSetEditorViewMixin,
    OperatingSystemFormSetEditorViewMixin,
)


# Cloud Capacity
class CloudCapacityEditorView(EditorView):
    editor_resource_list_url_reverse = "capacities:cloud_capacity_list"
    editor_url_reverse_base = "capacities:cloud_capacity_editor"
    editor_start_url_reverse_base = "capacities:new_cloud_capacity"
    editor_overview_url_reverse_base = "capacities:cloud_capacity_overview"
    resource_type_name_singular = "cloud capacity"
    resource_type_name_plural = "cloud capacities"
    api_client_class = CloudCapacityApiClient
    column_metadata_api_client_class = CloudCapacityColumnMetadataApiClient


class CloudCapacityEditorStartFormView(
    CloudCapacityEditorView, EditorStartFormView, FormView
):
    template_name = "capacities/new_cloud_capacity_start.html"
    form_class = CloudCapacityRegistrationForm


class CloudCapacityEditorProcessFormView(
    CloudCapacityEditorView, EditorProcessFormView
):
    template_name = "capacities/cloud_capacity_editor.html"
    main_form_class = CloudCapacityEditorForm
    success_url = reverse_lazy("capacities:new_cloud_capacity")


class CloudCapacityMetadataEditorProcessFormView(
    CloudCapacityEditorProcessFormView, CapacityMetadataEditorProcessFormView
):
    pass


class CloudCapacityCostAndLocalityEditorProcessFormView(
    CloudCapacityEditorProcessFormView, CapacityCostAndLocalityEditorProcessFormView
):
    pass


class CloudCapacityEnergyEditorProcessFormView(
    CloudCapacityEditorProcessFormView, CapacityEnergyEditorProcessFormView
):
    pass


class CloudCapacitySecurityTrustAndAccessEditorProcessFormView(
    CloudCapacityEditorProcessFormView,
    CapacitySecurityTrustAndAccessEditorProcessFormView,
):
    pass


class CloudCapacitySystemSpecificEditorProcessFormView(
    CloudCapacityEditorProcessFormView,
    MultipleEditorFormsetProcessFormView,
    ArchitectureFormSetEditorViewMixin,
    OperatingSystemFormSetEditorViewMixin,
):
    def dispatch(self, request, *args, **kwargs):
        self.add_architecture_formset_metadata()
        self.add_operating_system_formset_metadata()
        return super().dispatch(request, *args, **kwargs)


class CloudCapacitySpecsEditorProcessFormView(
    CloudCapacityEditorProcessFormView, CapacitySpecsEditorProcessFormView
):
    pass


class CloudCapacityEditorRouterView(CloudCapacityEditorView, CapacityEditorRouterView):
    editor_view_class = CloudCapacityEditorProcessFormView
    metadata_editor_view_class = CloudCapacityMetadataEditorProcessFormView
    cost_and_locality_editor_view_class = (
        CloudCapacityCostAndLocalityEditorProcessFormView
    )
    energy_editor_view_class = CloudCapacityEnergyEditorProcessFormView
    security_trust_and_access_editor_view_class = (
        CloudCapacitySecurityTrustAndAccessEditorProcessFormView
    )
    specs_editor_view_class = CloudCapacitySpecsEditorProcessFormView

    def route_to_view(self, request, *args, **kwargs):
        if self.category.lower() == "system specific":
            return CloudCapacitySystemSpecificEditorProcessFormView.as_view()(
                request, *args, **kwargs
            )
        return super().route_to_view(request, *args, **kwargs)


class CloudCapacityListFormView(CloudCapacityEditorView, ResourceListFormView):
    template_name = "capacities/cloud_capacities.html"
    new_resource_reverse = "capacities:new_cloud_capacity"


class CloudCapacityEditorOverviewTemplateView(
    CloudCapacityEditorView, EditorOverviewTemplateView
):
    template_name = "capacities/cloud_capacity_overview.html"
