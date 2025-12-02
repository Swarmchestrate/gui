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
#     CapacityResourceQuotaApiClient,
#     CapacityResourceQuotaColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    CapacityResourceQuotaApiClient,
    CapacityResourceQuotaColumnMetadataApiClient,
)
from .forms import (
    CapacityResourceQuotaRegistrationForm,
    CapacityResourceQuotaUpdateForm,
)
from .utils import (
    capacity_resource_quota_type_readable,
    capacity_resource_quota_type_readable_plural,
)


# Create your views here.
class CapacityResourceQuotaViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = CapacityResourceQuotaApiClient
    column_metadata_api_client_class = CapacityResourceQuotaColumnMetadataApiClient
    resource_list_reverse = "capacity_resource_quotas:capacity_resource_quota_list"
    resource_update_reverse = "capacity_resource_quotas:update_capacity_resource_quota"
    new_resource_reverse = "capacity_resource_quotas:new_capacity_resource_quota"
    resource_deletion_reverse = (
        "capacity_resource_quotas:delete_capacity_resource_quota"
    )
    multi_resource_deletion_reverse = (
        "capacity_resource_quotas:delete_capacity_resource_quotas"
    )
    resource_type_readable = capacity_resource_quota_type_readable()
    resource_type_readable_plural = capacity_resource_quota_type_readable_plural()


class CapacityResourceQuotaListFormView(
    CapacityResourceQuotaViewMixin, BasicResourceListFormView
):
    template_name = "capacity_resource_quotas/capacity_resource_quotas.html"
    new_resource_form_class = CapacityResourceQuotaRegistrationForm
    resource_update_form_class = CapacityResourceQuotaUpdateForm


class NewCapacityResourceQuotaFormView(
    CapacityResourceQuotaViewMixin, NewResourceFormView
):
    template_name = "capacity_resource_quotas/capacity_resource_quotas.html"
    new_resource_form_class = CapacityResourceQuotaRegistrationForm
    resource_update_form_class = CapacityResourceQuotaUpdateForm
    form_class = CapacityResourceQuotaRegistrationForm


class CapacityResourceQuotaUpdateFormView(
    CapacityResourceQuotaViewMixin, ResourceUpdateFormView
):
    template_name = "capacity_resource_quotas/capacity_resource_quotas.html"
    new_resource_form_class = CapacityResourceQuotaRegistrationForm
    resource_update_form_class = CapacityResourceQuotaUpdateForm
    form_class = CapacityResourceQuotaUpdateForm


class CapacityResourceQuotaDeletionFormView(
    CapacityResourceQuotaViewMixin, ResourceDeletionFormView
):
    pass


class MultiCapacityResourceQuotaDeletionFormView(
    CapacityResourceQuotaViewMixin, MultiResourceDeletionFormView
):
    pass
