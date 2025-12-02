from editor.forms.base_forms import OpenApiSpecificationBasedForm
from resource_management.forms import OpenApiSpecificationBasedFormWithIdAttributeSuffix

# from .api.api_clients import (
#     ApplicationBehaviourApiClient,
#     ApplicationBehaviourColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    ApplicationBehaviourApiClient,
    ApplicationBehaviourColumnMetadataApiClient,
)


class ApplicationBehaviourRegistrationForm(OpenApiSpecificationBasedForm):
    definition_name = "application_behaviour"

    def add_prefix(self, field_name):
        return "new-" + field_name


class ApplicationBehaviourUpdateForm(
    OpenApiSpecificationBasedFormWithIdAttributeSuffix
):
    definition_name = "application_behaviour"
