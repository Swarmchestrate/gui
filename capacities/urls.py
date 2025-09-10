from django.urls import path

from . import views


app_name = 'capacities'

urlpatterns = [
    path('cloud-capacities/', views.CloudCapacityRegistrationsTemplateView.as_view(), name='cloud_capacities_list'),
    path('cloud-capacities/<registration_id>/edit/', views.CloudCapacityEditorFormView.as_view(), name='cloud_capacity_editor'),
    path('new-cloud-capacity/', views.CloudCapacityEditorStartFormView.as_view(), name='new_cloud_capacity'),
    path('edge-capacities/', views.EdgeCapacityRegistrationsTemplateView.as_view(), name='edge_capacities_list'),
    path('edge-capacities/<registration_id>/edit/', views.EdgeCapacityEditorFormView.as_view(), name='edge_capacity_editor'),
    path('new-edge-capacity/', views.EdgeCapacityEditorStartFormView.as_view(), name='new_edge_capacity'),
]