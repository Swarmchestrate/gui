from django.urls import path

from . import views

app_name = "capacity_instance_types"

urlpatterns = [
    path(
        "capacity-instance-types/",
        views.CapacityInstanceTypeListFormView.as_view(),
        name="capacity_instance_type_list",
    ),
    path(
        "capacity-instance-types/new/",
        views.NewCapacityInstanceTypeFormView.as_view(),
        name="new_capacity_instance_type",
    ),
    path(
        "capacity-instance-types/deletes/",
        views.MultiCapacityInstanceTypeDeletionFormView.as_view(),
        name="delete_capacity_instance_types",
    ),
    path(
        "capacity-instance-types/<resource_id>/edit/",
        views.CapacityInstanceTypeUpdateFormView.as_view(),
        name="update_capacity_instance_type",
    ),
    path(
        "capacity-instance-types/<resource_id>/delete/",
        views.CapacityInstanceTypeDeletionFormView.as_view(),
        name="delete_capacity_instance_type",
    ),
]
