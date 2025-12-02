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
#     CapacityPriceApiClient,
#     CapacityPriceColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    CapacityPriceApiClient,
    CapacityPriceColumnMetadataApiClient,
)
from .forms import (
    CapacityPriceRegistrationForm,
    CapacityPriceUpdateForm,
)
from .utils import (
    capacity_price_type_readable,
    capacity_price_type_readable_plural,
)


# Create your views here.
class CapacityPriceViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = CapacityPriceApiClient
    column_metadata_api_client_class = CapacityPriceColumnMetadataApiClient
    resource_list_reverse = "capacity_prices:capacity_price_list"
    resource_update_reverse = "capacity_prices:update_capacity_price"
    new_resource_reverse = "capacity_prices:new_capacity_price"
    resource_deletion_reverse = "capacity_prices:delete_capacity_price"
    multi_resource_deletion_reverse = "capacity_prices:delete_capacity_prices"
    resource_type_readable = capacity_price_type_readable()
    resource_type_readable_plural = capacity_price_type_readable_plural()


class CapacityPriceListFormView(CapacityPriceViewMixin, BasicResourceListFormView):
    template_name = "capacity_prices/capacity_prices.html"
    new_resource_form_class = CapacityPriceRegistrationForm
    resource_update_form_class = CapacityPriceUpdateForm


class NewCapacityPriceFormView(CapacityPriceViewMixin, NewResourceFormView):
    template_name = "capacity_prices/capacity_prices.html"
    new_resource_form_class = CapacityPriceRegistrationForm
    resource_update_form_class = CapacityPriceUpdateForm
    form_class = CapacityPriceRegistrationForm


class CapacityPriceUpdateFormView(CapacityPriceViewMixin, ResourceUpdateFormView):
    template_name = "capacity_prices/capacity_prices.html"
    new_resource_form_class = CapacityPriceRegistrationForm
    resource_update_form_class = CapacityPriceUpdateForm
    form_class = CapacityPriceUpdateForm


class CapacityPriceDeletionFormView(CapacityPriceViewMixin, ResourceDeletionFormView):
    pass


class MultiCapacityPriceDeletionFormView(
    CapacityPriceViewMixin, MultiResourceDeletionFormView
):
    pass
