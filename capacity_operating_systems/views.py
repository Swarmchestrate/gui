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
#     CapacityOperatingSystemApiClient,
#     CapacityOperatingSystemColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    CapacityOperatingSystemApiClient,
    CapacityOperatingSystemColumnMetadataApiClient,
)
from .forms import (
    CapacityOperatingSystemRegistrationForm,
    CapacityOperatingSystemUpdateForm,
)
from .utils import (
    capacity_operating_system_type_readable,
    capacity_operating_system_type_readable_plural,
)


# Create your views here.
class CapacityOperatingSystemViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = CapacityOperatingSystemApiClient
    column_metadata_api_client_class = CapacityOperatingSystemColumnMetadataApiClient
    resource_list_reverse = "capacity_operating_systems:capacity_operating_system_list"
    resource_update_reverse = (
        "capacity_operating_systems:update_capacity_operating_system"
    )
    new_resource_reverse = "capacity_operating_systems:new_capacity_operating_system"
    resource_deletion_reverse = (
        "capacity_operating_systems:delete_capacity_operating_system"
    )
    multi_resource_deletion_reverse = (
        "capacity_operating_systems:delete_capacity_operating_systems"
    )
    resource_type_readable = capacity_operating_system_type_readable()
    resource_type_readable_plural = capacity_operating_system_type_readable_plural()


class CapacityOperatingSystemListFormView(
    CapacityOperatingSystemViewMixin, BasicResourceListFormView
):
    template_name = "capacity_operating_systems/capacity_operating_systems.html"
    new_resource_form_class = CapacityOperatingSystemRegistrationForm
    resource_update_form_class = CapacityOperatingSystemUpdateForm


class NewCapacityOperatingSystemFormView(
    CapacityOperatingSystemViewMixin, NewResourceFormView
):
    template_name = "capacity_operating_systems/capacity_operating_systems.html"
    new_resource_form_class = CapacityOperatingSystemRegistrationForm
    resource_update_form_class = CapacityOperatingSystemUpdateForm
    form_class = CapacityOperatingSystemRegistrationForm


class CapacityOperatingSystemUpdateFormView(
    CapacityOperatingSystemViewMixin, ResourceUpdateFormView
):
    template_name = "capacity_operating_systems/capacity_operating_systems.html"
    new_resource_form_class = CapacityOperatingSystemRegistrationForm
    resource_update_form_class = CapacityOperatingSystemUpdateForm
    form_class = CapacityOperatingSystemUpdateForm


class CapacityOperatingSystemDeletionFormView(
    CapacityOperatingSystemViewMixin, ResourceDeletionFormView
):
    pass


class MultiCapacityOperatingSystemDeletionFormView(
    CapacityOperatingSystemViewMixin, MultiResourceDeletionFormView
):
    pass
