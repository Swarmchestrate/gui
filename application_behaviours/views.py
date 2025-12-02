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
#     ApplicationBehaviourApiClient,
#     ApplicationBehaviourColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    ApplicationBehaviourApiClient,
    ApplicationBehaviourColumnMetadataApiClient,
)
from .forms import (
    ApplicationBehaviourRegistrationForm,
    ApplicationBehaviourUpdateForm,
)
from .utils import (
    application_behaviour_type_readable,
    application_behaviour_type_readable_plural,
)


# Create your views here.
class ApplicationBehaviourViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = ApplicationBehaviourApiClient
    column_metadata_api_client_class = ApplicationBehaviourColumnMetadataApiClient
    resource_list_reverse = "application_behaviours:application_behaviour_list"
    resource_update_reverse = "application_behaviours:update_application_behaviour"
    new_resource_reverse = "application_behaviours:new_application_behaviour"
    resource_deletion_reverse = "application_behaviours:delete_application_behaviour"
    multi_resource_deletion_reverse = (
        "application_behaviours:delete_application_behaviours"
    )
    resource_type_readable = application_behaviour_type_readable()
    resource_type_readable_plural = application_behaviour_type_readable_plural()


class ApplicationBehaviourListFormView(
    ApplicationBehaviourViewMixin, BasicResourceListFormView
):
    template_name = "application_behaviours/application_behaviours.html"
    new_resource_form_class = ApplicationBehaviourRegistrationForm
    resource_update_form_class = ApplicationBehaviourUpdateForm


class NewApplicationBehaviourFormView(
    ApplicationBehaviourViewMixin, NewResourceFormView
):
    template_name = "application_behaviours/application_behaviours.html"
    new_resource_form_class = ApplicationBehaviourRegistrationForm
    resource_update_form_class = ApplicationBehaviourUpdateForm
    form_class = ApplicationBehaviourRegistrationForm


class ApplicationBehaviourUpdateFormView(
    ApplicationBehaviourViewMixin, ResourceUpdateFormView
):
    template_name = "application_behaviours/application_behaviours.html"
    new_resource_form_class = ApplicationBehaviourRegistrationForm
    resource_update_form_class = ApplicationBehaviourUpdateForm
    form_class = ApplicationBehaviourUpdateForm


class ApplicationBehaviourDeletionFormView(
    ApplicationBehaviourViewMixin, ResourceDeletionFormView
):
    pass


class MultiApplicationBehaviourDeletionFormView(
    ApplicationBehaviourViewMixin, MultiResourceDeletionFormView
):
    pass
