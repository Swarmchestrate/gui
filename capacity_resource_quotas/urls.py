from django.urls import path

from . import views

app_name = "capacity_resource_quotas"

urlpatterns = [
    path(
        "capacity-resource-quotas/",
        views.CapacityResourceQuotaListFormView.as_view(),
        name="capacity_resource_quota_list",
    ),
    path(
        "capacity-resource-quotas/new/",
        views.NewCapacityResourceQuotaFormView.as_view(),
        name="new_capacity_resource_quota",
    ),
    path(
        "capacity-resource-quotas/deletes/",
        views.MultiCapacityResourceQuotaDeletionFormView.as_view(),
        name="delete_capacity_resource_quotas",
    ),
    path(
        "capacity-resource-quotas/<resource_id>/edit/",
        views.CapacityResourceQuotaUpdateFormView.as_view(),
        name="update_capacity_resource_quota",
    ),
    path(
        "capacity-resource-quotas/<resource_id>/delete/",
        views.CapacityResourceQuotaDeletionFormView.as_view(),
        name="delete_capacity_resource_quota",
    ),
]
