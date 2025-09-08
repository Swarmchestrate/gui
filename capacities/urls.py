from django.urls import path

from . import views


app_name = 'capacities'

urlpatterns = [
    path('new-cloud-capacity/', views.CloudCapacityEditorStartFormView.as_view(), name='new_cloud_capacity'),
    path('new-cloud-capacity/<registration_id>/<field_format>/', views.CloudCapacityEditorFormView.as_view(), name='new_cloud_capacity'),
    path('new-edge-capacity/', views.EdgeCapacityEditorStartFormView.as_view(), name='new_edge_capacity'),
    path('new-edge-capacity/<registration_id>/<field_format>/', views.EdgeCapacityEditorFormView.as_view(), name='new_edge_capacity'),
]