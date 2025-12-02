from django.urls import path

from . import views

app_name = "capacity_operating_systems"

urlpatterns = [
    path(
        "capacity-operating-systems/",
        views.CapacityOperatingSystemListFormView.as_view(),
        name="capacity_operating_system_list",
    ),
    path(
        "capacity-operating-systems/new/",
        views.NewCapacityOperatingSystemFormView.as_view(),
        name="new_capacity_operating_system",
    ),
    path(
        "capacity-operating-systems/deletes/",
        views.MultiCapacityOperatingSystemDeletionFormView.as_view(),
        name="delete_capacity_operating_systems",
    ),
    path(
        "capacity-operating-systems/<resource_id>/edit/",
        views.CapacityOperatingSystemUpdateFormView.as_view(),
        name="update_capacity_operating_system",
    ),
    path(
        "capacity-operating-systems/<resource_id>/delete/",
        views.CapacityOperatingSystemDeletionFormView.as_view(),
        name="delete_capacity_operating_system",
    ),
]
