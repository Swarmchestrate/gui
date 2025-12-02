from editor.base_views import (
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    ResourceTypeNameContextMixin,
)
from resource_management.views import (
    BasicResourceListFormView,
    MultiResourceDeletionFormView,
    NewResourceFormView,
    ResourceDeletionFormView,
    ResourceListContextMixin,
    ResourceUpdateFormView,
)

# from .api.api_clients import (
#     CapacityEnergyConsumptionApiClient,
#     CapacityEnergyConsumptionColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    CapacityEnergyConsumptionApiClient,
    CapacityEnergyConsumptionColumnMetadataApiClient,
)
from .forms import (
    CapacityEnergyConsumptionRegistrationForm,
    CapacityEnergyConsumptionUpdateForm,
)
from .utils import (
    capacity_energy_consumption_type_readable,
    capacity_energy_consumption_type_readable_plural,
)


# Create your views here.
class CapacityEnergyConsumptionViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = CapacityEnergyConsumptionApiClient
    column_metadata_api_client_class = CapacityEnergyConsumptionColumnMetadataApiClient
    resource_list_reverse = (
        "capacity_energy_consumptions:capacity_energy_consumption_list"
    )
    resource_update_reverse = (
        "capacity_energy_consumptions:update_capacity_energy_consumption"
    )
    new_resource_reverse = (
        "capacity_energy_consumptions:new_capacity_energy_consumption"
    )
    resource_deletion_reverse = (
        "capacity_energy_consumptions:delete_capacity_energy_consumption"
    )
    multi_resource_deletion_reverse = (
        "capacity_energy_consumptions:delete_capacity_energy_consumptions"
    )
    resource_type_readable = capacity_energy_consumption_type_readable()
    resource_type_readable_plural = capacity_energy_consumption_type_readable_plural()


class CapacityEnergyConsumptionListFormView(
    CapacityEnergyConsumptionViewMixin, BasicResourceListFormView
):
    template_name = "capacity_energy_consumptions/capacity_energy_consumptions.html"
    new_resource_form_class = CapacityEnergyConsumptionRegistrationForm
    resource_update_form_class = CapacityEnergyConsumptionUpdateForm


class NewCapacityEnergyConsumptionFormView(
    CapacityEnergyConsumptionViewMixin, NewResourceFormView
):
    template_name = "capacity_energy_consumptions/capacity_energy_consumptions.html"
    new_resource_form_class = CapacityEnergyConsumptionRegistrationForm
    resource_update_form_class = CapacityEnergyConsumptionUpdateForm
    form_class = CapacityEnergyConsumptionRegistrationForm


class CapacityEnergyConsumptionUpdateFormView(
    CapacityEnergyConsumptionViewMixin, ResourceUpdateFormView
):
    template_name = "capacity_energy_consumptions/capacity_energy_consumptions.html"
    new_resource_form_class = CapacityEnergyConsumptionRegistrationForm
    resource_update_form_class = CapacityEnergyConsumptionUpdateForm
    form_class = CapacityEnergyConsumptionUpdateForm


class CapacityEnergyConsumptionDeletionFormView(
    CapacityEnergyConsumptionViewMixin, ResourceDeletionFormView
):
    pass


class MultiCapacityEnergyConsumptionDeletionFormView(
    CapacityEnergyConsumptionViewMixin, MultiResourceDeletionFormView
):
    pass
