from django.urls import path

from . import views


app_name = 'capacities'

urlpatterns = [
    path('cloud-capacities/', views.CloudCapacityRegistrationsListFormView.as_view(), name='cloud_capacities_list'),
    path('cloud-capacities/<registration_id>/edit/', views.CloudCapacityEditorRouterView.as_view(), name='cloud_capacity_editor'),
    path('cloud-capacities/<registration_id>/overview/', views.CloudCapacityEditorOverviewTemplateView.as_view(), name='cloud_capacity_overview'),
    path('new-cloud-capacity/', views.CloudCapacityEditorStartFormView.as_view(), name='new_cloud_capacity'),
    path('edge-capacities/', views.EdgeCapacityRegistrationsListFormView.as_view(), name='edge_capacities_list'),
    path('edge-capacities/<registration_id>/edit/', views.EdgeCapacityEditorProcessFormView.as_view(), name='edge_capacity_editor'),
    path('edge-capacities/<registration_id>/overview/', views.EdgeCapacityEditorOverviewTemplateView.as_view(), name='edge_capacity_overview'),
    path('new-edge-capacity/', views.EdgeCapacityEditorStartFormView.as_view(), name='new_edge_capacity'),
]
