from editor.forms.base_forms import OpenApiSpecificationBasedForm
from resource_management.forms import OpenApiSpecificationBasedFormWithIdAttributeSuffix

# from .api.api_clients import (
#     CapacityPriceApiClient,
#     CapacityPriceColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    CapacityPriceApiClient,
    CapacityPriceColumnMetadataApiClient,
)


class CapacityPriceRegistrationForm(OpenApiSpecificationBasedForm):
    definition_name = "capacity_price"

    def add_prefix(self, field_name):
        return "new-" + field_name


class CapacityPriceUpdateForm(OpenApiSpecificationBasedFormWithIdAttributeSuffix):
    definition_name = "capacity_price"
