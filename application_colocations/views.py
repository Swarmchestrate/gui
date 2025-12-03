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
#     ApplicationColocationApiClient,
#     ApplicationColocationColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    ApplicationColocateApiClient,
    ApplicationColocateColumnMetadataApiClient,
)
from .forms import (
    ApplicationColocationRegistrationForm,
    ApplicationColocationUpdateForm,
)
from .utils import (
    application_colocation_type_readable,
    application_colocation_type_readable_plural,
)


# Create your views here.
class ApplicationColocationViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = ApplicationColocateApiClient
    column_metadata_api_client_class = ApplicationColocateColumnMetadataApiClient
    resource_list_reverse = "application_colocations:application_colocation_list"
    resource_update_reverse = "application_colocations:update_application_colocation"
    new_resource_reverse = "application_colocations:new_application_colocation"
    resource_deletion_reverse = "application_colocations:delete_application_colocation"
    multi_resource_deletion_reverse = (
        "application_colocations:delete_application_colocations"
    )
    resource_type_readable = application_colocation_type_readable()
    resource_type_readable_plural = application_colocation_type_readable_plural()


class ApplicationColocationListFormView(
    ApplicationColocationViewMixin, BasicResourceListFormView
):
    template_name = "application_colocations/application_colocations.html"
    new_resource_form_class = ApplicationColocationRegistrationForm
    resource_update_form_class = ApplicationColocationUpdateForm


class NewApplicationColocationFormView(
    ApplicationColocationViewMixin, NewResourceFormView
):
    template_name = "application_colocations/application_colocations.html"
    new_resource_form_class = ApplicationColocationRegistrationForm
    resource_update_form_class = ApplicationColocationUpdateForm
    form_class = ApplicationColocationRegistrationForm


class ApplicationColocationUpdateFormView(
    ApplicationColocationViewMixin, ResourceUpdateFormView
):
    template_name = "application_colocations/application_colocations.html"
    new_resource_form_class = ApplicationColocationRegistrationForm
    resource_update_form_class = ApplicationColocationUpdateForm
    form_class = ApplicationColocationUpdateForm


class ApplicationColocationDeletionFormView(
    ApplicationColocationViewMixin, ResourceDeletionFormView
):
    pass


class MultiApplicationColocationDeletionFormView(
    ApplicationColocationViewMixin, MultiResourceDeletionFormView
):
    pass
