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
        "cloud-capacities/new/",
        cloud_capacity_views.CloudCapacityEditorStartFormView.as_view(),
        name="new_cloud_capacity",
    ),
    path(
        "cloud-capacities/deletes/",
        cloud_capacity_views.MultiCloudCapacityDeletionFormView.as_view(),
        name="delete_cloud_capacities",
    ),
    path(
        "cloud-capacities/<resource_id>/overview/",
        cloud_capacity_views.CloudCapacityEditorOverviewTemplateView.as_view(),
        name="cloud_capacity_overview",
    ),
    path(
        "cloud-capacities/<resource_id>/edit/",
        cloud_capacity_views.CloudCapacityEditorProcessFormView.as_view(),
        name="cloud_capacity_editor",
    ),
    path(
        "cloud-capacities/<resource_id>/delete/",
        cloud_capacity_views.CloudCapacityDeletionFormView.as_view(),
        name="delete_cloud_capacity",
    ),
    path(
        "edge-capacities/",
        edge_capacity_views.EdgeCapacityListFormView.as_view(),
        name="edge_capacity_list",
    ),
    path(
        "edge-capacities/new/",
        edge_capacity_views.EdgeCapacityEditorStartFormView.as_view(),
        name="new_edge_capacity",
    ),
    path(
        "edge-capacities/deletes/",
        edge_capacity_views.MultiEdgeCapacityDeletionFormView.as_view(),
        name="delete_edge_capacities",
    ),
    path(
        "edge-capacities/<resource_id>/overview/",
        edge_capacity_views.EdgeCapacityEditorOverviewTemplateView.as_view(),
        name="edge_capacity_overview",
    ),
    path(
        "edge-capacities/<resource_id>/edit/",
        edge_capacity_views.EdgeCapacityEditorProcessFormView.as_view(),
        name="edge_capacity_editor",
    ),
    path(
        "edge-capacities/<resource_id>/delete/",
        edge_capacity_views.EdgeCapacityDeletionFormView.as_view(),
        name="delete_edge_capacity",
    ),
]
