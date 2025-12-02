from editor.forms.base_forms import OpenApiSpecificationBasedForm
from resource_management.forms import OpenApiSpecificationBasedFormWithIdAttributeSuffix

# from .api.api_clients import (
#     CapacityResourceQuotaApiClient,
#     CapacityResourceQuotaColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    CapacityResourceQuotaApiClient,
    CapacityResourceQuotaColumnMetadataApiClient,
)


class CapacityResourceQuotaRegistrationForm(OpenApiSpecificationBasedForm):
    definition_name = "capacity_resource_quota"

    def add_prefix(self, field_name):
        return "new-" + field_name


class CapacityResourceQuotaUpdateForm(
    OpenApiSpecificationBasedFormWithIdAttributeSuffix
):
    definition_name = "capacity_resource_quota"
