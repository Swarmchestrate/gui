from editor.forms.base_forms import OpenApiSpecificationBasedForm
from resource_management.forms import OpenApiSpecificationBasedFormWithIdAttributeSuffix

# from .api.api_clients import (
#     CapacityOperatingSystemApiClient,
#     CapacityOperatingSystemColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    CapacityOperatingSystemApiClient,
    CapacityOperatingSystemColumnMetadataApiClient,
)


class CapacityOperatingSystemRegistrationForm(OpenApiSpecificationBasedForm):
    definition_name = "capacity_operating_system"

    def add_prefix(self, field_name):
        return "new-" + field_name


class CapacityOperatingSystemUpdateForm(
    OpenApiSpecificationBasedFormWithIdAttributeSuffix
):
    definition_name = "capacity_operating_system"
