from django.urls import path

from . import views

app_name = "capacity_prices"

urlpatterns = [
    path(
        "capacity-prices/",
        views.CapacityPriceListFormView.as_view(),
        name="capacity_price_list",
    ),
    path(
        "capacity-prices/new/",
        views.NewCapacityPriceFormView.as_view(),
        name="new_capacity_price",
    ),
    path(
        "capacity-prices/deletes/",
        views.MultiCapacityPriceDeletionFormView.as_view(),
        name="delete_capacity_prices",
    ),
    path(
        "capacity-prices/<resource_id>/edit/",
        views.CapacityPriceUpdateFormView.as_view(),
        name="update_capacity_price",
    ),
    path(
        "capacity-prices/<resource_id>/delete/",
        views.CapacityPriceDeletionFormView.as_view(),
        name="delete_capacity_price",
    ),
]
