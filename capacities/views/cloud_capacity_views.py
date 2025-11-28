from dataclasses import dataclass

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
    ResourceDeletionFormView,
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
from .mixins.cloud_capacity_mixins import (
    ArchitectureFormSetEditorViewMixin,
    OperatingSystemFormSetEditorViewMixin,
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
    resource_type_name_singular = "cloud capacity"
    resource_type_name_plural = "cloud capacities"


class CloudCapacityEditorStartFormView(
    CloudCapacityViewMixin, EditorStartFormView, FormView
):
    template_name = "capacities/new_cloud_capacity_start.html"
    form_class = CloudCapacityRegistrationForm


class CloudCapacityEditorProcessFormView(CloudCapacityViewMixin, EditorProcessFormView):
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


class CloudCapacityEditorRouterView(CloudCapacityViewMixin, CapacityEditorRouterView):
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
