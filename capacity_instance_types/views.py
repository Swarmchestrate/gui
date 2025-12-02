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
#     CapacityInstanceTypeApiClient,
#     CapacityInstanceTypeColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    CapacityInstanceTypeApiClient,
    CapacityInstanceTypeColumnMetadataApiClient,
)
from .forms import CapacityInstanceTypeRegistrationForm, CapacityInstanceTypeUpdateForm
from .utils import (
    capacity_instance_type_type_readable,
    capacity_instance_type_type_readable_plural,
)


class CapacityInstanceTypeViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = CapacityInstanceTypeApiClient
    column_metadata_api_client_class = CapacityInstanceTypeColumnMetadataApiClient
    resource_list_reverse = "capacity_instance_types:capacity_instance_type_list"
    resource_update_reverse = "capacity_instance_types:update_capacity_instance_type"
    new_resource_reverse = "capacity_instance_types:new_capacity_instance_type"
    resource_deletion_reverse = "capacity_instance_types:delete_capacity_instance_type"
    multi_resource_deletion_reverse = (
        "capacity_instance_types:delete_capacity_instance_types"
    )
    resource_type_readable = capacity_instance_type_type_readable()
    resource_type_readable_plural = capacity_instance_type_type_readable_plural()


class CapacityInstanceTypeListFormView(
    CapacityInstanceTypeViewMixin, BasicResourceListFormView
):
    template_name = "capacity_instance_types/capacity_instance_types.html"
    new_resource_form_class = CapacityInstanceTypeRegistrationForm
    resource_update_form_class = CapacityInstanceTypeUpdateForm


class NewCapacityInstanceTypeFormView(
    CapacityInstanceTypeViewMixin, NewResourceFormView
):
    template_name = "capacity_instance_types/capacity_instance_types.html"
    new_resource_form_class = CapacityInstanceTypeRegistrationForm
    resource_update_form_class = CapacityInstanceTypeUpdateForm
    form_class = CapacityInstanceTypeRegistrationForm


class CapacityInstanceTypeUpdateFormView(
    CapacityInstanceTypeViewMixin, ResourceUpdateFormView
):
    template_name = "capacity_instance_types/capacity_instance_types.html"
    new_resource_form_class = CapacityInstanceTypeRegistrationForm
    resource_update_form_class = CapacityInstanceTypeUpdateForm
    form_class = CapacityInstanceTypeUpdateForm


class CapacityInstanceTypeDeletionFormView(
    CapacityInstanceTypeViewMixin, ResourceDeletionFormView
):
    pass


class MultiCapacityInstanceTypeDeletionFormView(
    CapacityInstanceTypeViewMixin, MultiResourceDeletionFormView
):
    pass
