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
#     ApplicationVolumeApiClient,
#     ApplicationVolumeColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    ApplicationVolumeApiClient,
    ApplicationVolumeColumnMetadataApiClient,
)
from .forms import (
    ApplicationVolumeRegistrationForm,
    ApplicationVolumeUpdateForm,
)
from .utils import (
    application_volume_type_readable,
    application_volume_type_readable_plural,
)


# Create your views here.
class ApplicationVolumeViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = ApplicationVolumeApiClient
    column_metadata_api_client_class = ApplicationVolumeColumnMetadataApiClient
    resource_list_reverse = "application_volumes:application_volume_list"
    resource_update_reverse = "application_volumes:update_application_volume"
    new_resource_reverse = "application_volumes:new_application_volume"
    resource_deletion_reverse = "application_volumes:delete_application_volume"
    multi_resource_deletion_reverse = "application_volumes:delete_application_volumes"
    resource_type_readable = application_volume_type_readable()
    resource_type_readable_plural = application_volume_type_readable_plural()


class ApplicationVolumeListFormView(
    ApplicationVolumeViewMixin, BasicResourceListFormView
):
    template_name = "application_volumes/application_volumes.html"
    new_resource_form_class = ApplicationVolumeRegistrationForm
    resource_update_form_class = ApplicationVolumeUpdateForm


class NewApplicationVolumeFormView(ApplicationVolumeViewMixin, NewResourceFormView):
    template_name = "application_volumes/application_volumes.html"
    new_resource_form_class = ApplicationVolumeRegistrationForm
    resource_update_form_class = ApplicationVolumeUpdateForm
    form_class = ApplicationVolumeRegistrationForm


class ApplicationVolumeUpdateFormView(
    ApplicationVolumeViewMixin, ResourceUpdateFormView
):
    template_name = "application_volumes/application_volumes.html"
    new_resource_form_class = ApplicationVolumeRegistrationForm
    resource_update_form_class = ApplicationVolumeUpdateForm
    form_class = ApplicationVolumeUpdateForm


class ApplicationVolumeDeletionFormView(
    ApplicationVolumeViewMixin, ResourceDeletionFormView
):
    pass


class MultiApplicationVolumeDeletionFormView(
    ApplicationVolumeViewMixin, MultiResourceDeletionFormView
):
    pass
