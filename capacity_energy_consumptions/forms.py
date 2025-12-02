from editor.forms.base_forms import OpenApiSpecificationBasedForm
from resource_management.forms import OpenApiSpecificationBasedFormWithIdAttributeSuffix

# from .api.api_clients import (
#     CapacityEnergyConsumptionApiClient,
#     CapacityEnergyConsumptionColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    CapacityEnergyConsumptionApiClient,
    CapacityEnergyConsumptionColumnMetadataApiClient,
)


class CapacityEnergyConsumptionRegistrationForm(OpenApiSpecificationBasedForm):
    definition_name = "capacity_energy_consumption"

    def add_prefix(self, field_name):
        return "new-" + field_name


class CapacityEnergyConsumptionUpdateForm(
    OpenApiSpecificationBasedFormWithIdAttributeSuffix
):
    definition_name = "capacity_energy_consumption"
