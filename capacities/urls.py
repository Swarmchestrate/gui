from django.urls import path

from .views import (
    cloud_capacity_views,
    edge_capacity_views,
)

app_name = "capacities"

urlpatterns = [
    path(
        "cloud-capacities/",
        cloud_capacity_views.CloudCapacityListFormView.as_view(),
        name="cloud_capacity_list",
    ),
    path(
        "cloud-capacities/<resource_id>/edit/",
        cloud_capacity_views.CloudCapacityEditorRouterView.as_view(),
        name="cloud_capacity_editor",
    ),
    path(
        "cloud-capacities/<resource_id>/overview/",
        cloud_capacity_views.CloudCapacityEditorOverviewTemplateView.as_view(),
        name="cloud_capacity_overview",
    ),
    path(
        "new-cloud-capacity/",
        cloud_capacity_views.CloudCapacityEditorStartFormView.as_view(),
        name="new_cloud_capacity",
    ),
    path(
        "edge-capacities/",
        edge_capacity_views.EdgeCapacityListFormView.as_view(),
        name="edge_capacity_list",
    ),
    path(
        "edge-capacities/<resource_id>/edit/",
        edge_capacity_views.EdgeCapacityEditorRouterView.as_view(),
        name="edge_capacity_editor",
    ),
    path(
        "edge-capacities/<resource_id>/overview/",
        edge_capacity_views.EdgeCapacityEditorOverviewTemplateView.as_view(),
        name="edge_capacity_overview",
    ),
    path(
        "new-edge-capacity/",
        edge_capacity_views.EdgeCapacityEditorStartFormView.as_view(),
        name="new_edge_capacity",
    ),
]
