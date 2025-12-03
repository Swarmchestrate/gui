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
#     ApplicationPrefResourceProviderApiClient,
#     ApplicationPrefResourceProviderColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    ApplicationPrefResourceProviderApiClient,
    ApplicationPrefResourceProviderColumnMetadataApiClient,
)
from .forms import (
    ApplicationPrefResourceProviderRegistrationForm,
    ApplicationPrefResourceProviderUpdateForm,
)
from .utils import (
    application_pref_resource_provider_type_readable,
    application_pref_resource_provider_type_readable_plural,
)


# Create your views here.
class ApplicationPrefResourceProviderViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = ApplicationPrefResourceProviderApiClient
    column_metadata_api_client_class = (
        ApplicationPrefResourceProviderColumnMetadataApiClient
    )
    resource_list_reverse = (
        "application_pref_resource_providers:application_pref_resource_provider_list"
    )
    resource_update_reverse = (
        "application_pref_resource_providers:update_application_pref_resource_provider"
    )
    new_resource_reverse = (
        "application_pref_resource_providers:new_application_pref_resource_provider"
    )
    resource_deletion_reverse = (
        "application_pref_resource_providers:delete_application_pref_resource_provider"
    )
    multi_resource_deletion_reverse = (
        "application_pref_resource_providers:delete_application_pref_resource_providers"
    )
    resource_type_readable = application_pref_resource_provider_type_readable()
    resource_type_readable_plural = (
        application_pref_resource_provider_type_readable_plural()
    )


class ApplicationPrefResourceProviderListFormView(
    ApplicationPrefResourceProviderViewMixin, BasicResourceListFormView
):
    template_name = (
        "application_pref_resource_providers/application_pref_resource_providers.html"
    )
    new_resource_form_class = ApplicationPrefResourceProviderRegistrationForm
    resource_update_form_class = ApplicationPrefResourceProviderUpdateForm


class NewApplicationPrefResourceProviderFormView(
    ApplicationPrefResourceProviderViewMixin, NewResourceFormView
):
    template_name = (
        "application_pref_resource_providers/application_pref_resource_providers.html"
    )
    new_resource_form_class = ApplicationPrefResourceProviderRegistrationForm
    resource_update_form_class = ApplicationPrefResourceProviderUpdateForm
    form_class = ApplicationPrefResourceProviderRegistrationForm


class ApplicationPrefResourceProviderUpdateFormView(
    ApplicationPrefResourceProviderViewMixin, ResourceUpdateFormView
):
    template_name = (
        "application_pref_resource_providers/application_pref_resource_providers.html"
    )
    new_resource_form_class = ApplicationPrefResourceProviderRegistrationForm
    resource_update_form_class = ApplicationPrefResourceProviderUpdateForm
    form_class = ApplicationPrefResourceProviderUpdateForm


class ApplicationPrefResourceProviderDeletionFormView(
    ApplicationPrefResourceProviderViewMixin, ResourceDeletionFormView
):
    pass


class MultiApplicationPrefResourceProviderDeletionFormView(
    ApplicationPrefResourceProviderViewMixin, MultiResourceDeletionFormView
):
    pass
