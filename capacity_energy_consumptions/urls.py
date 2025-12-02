from django.urls import path

from . import views

app_name = "capacity_energy_consumptions"

urlpatterns = [
    path(
        "capacity-energy-consumptions/",
        views.CapacityEnergyConsumptionListFormView.as_view(),
        name="capacity_energy_consumption_list",
    ),
    path(
        "capacity-energy-consumptions/new/",
        views.NewCapacityEnergyConsumptionFormView.as_view(),
        name="new_capacity_energy_consumption",
    ),
    path(
        "capacity-energy-consumptions/deletes/",
        views.MultiCapacityEnergyConsumptionDeletionFormView.as_view(),
        name="delete_capacity_energy_consumptions",
    ),
    path(
        "capacity-energy-consumptions/<resource_id>/edit/",
        views.CapacityEnergyConsumptionUpdateFormView.as_view(),
        name="update_capacity_energy_consumption",
    ),
    path(
        "capacity-energy-consumptions/<resource_id>/delete/",
        views.CapacityEnergyConsumptionDeletionFormView.as_view(),
        name="delete_capacity_energy_consumption",
    ),
]
