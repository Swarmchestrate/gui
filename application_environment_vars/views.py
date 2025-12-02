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
#     ApplicationEnvironmentVarApiClient,
#     ApplicationEnvironmentVarColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    ApplicationEnvironmentVarApiClient,
    ApplicationEnvironmentVarColumnMetadataApiClient,
)
from .forms import (
    ApplicationEnvironmentVarRegistrationForm,
    ApplicationEnvironmentVarUpdateForm,
)
from .utils import (
    application_environment_var_type_readable,
    application_environment_var_type_readable_plural,
)


# Create your views here.
class ApplicationEnvironmentVarViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = ApplicationEnvironmentVarApiClient
    column_metadata_api_client_class = ApplicationEnvironmentVarColumnMetadataApiClient
    resource_list_reverse = (
        "application_environment_vars:application_environment_var_list"
    )
    resource_update_reverse = (
        "application_environment_vars:update_application_environment_var"
    )
    new_resource_reverse = (
        "application_environment_vars:new_application_environment_var"
    )
    resource_deletion_reverse = (
        "application_environment_vars:delete_application_environment_var"
    )
    multi_resource_deletion_reverse = (
        "application_environment_vars:delete_application_environment_vars"
    )
    resource_type_readable = application_environment_var_type_readable()
    resource_type_readable_plural = application_environment_var_type_readable_plural()


class ApplicationEnvironmentVarListFormView(
    ApplicationEnvironmentVarViewMixin, BasicResourceListFormView
):
    template_name = "application_environment_vars/application_environment_vars.html"
    new_resource_form_class = ApplicationEnvironmentVarRegistrationForm
    resource_update_form_class = ApplicationEnvironmentVarUpdateForm


class NewApplicationEnvironmentVarFormView(
    ApplicationEnvironmentVarViewMixin, NewResourceFormView
):
    template_name = "application_environment_vars/application_environment_vars.html"
    new_resource_form_class = ApplicationEnvironmentVarRegistrationForm
    resource_update_form_class = ApplicationEnvironmentVarUpdateForm
    form_class = ApplicationEnvironmentVarRegistrationForm


class ApplicationEnvironmentVarUpdateFormView(
    ApplicationEnvironmentVarViewMixin, ResourceUpdateFormView
):
    template_name = "application_environment_vars/application_environment_vars.html"
    new_resource_form_class = ApplicationEnvironmentVarRegistrationForm
    resource_update_form_class = ApplicationEnvironmentVarUpdateForm
    form_class = ApplicationEnvironmentVarUpdateForm


class ApplicationEnvironmentVarDeletionFormView(
    ApplicationEnvironmentVarViewMixin, ResourceDeletionFormView
):
    pass


class MultiApplicationEnvironmentVarDeletionFormView(
    ApplicationEnvironmentVarViewMixin, MultiResourceDeletionFormView
):
    pass
