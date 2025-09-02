from django.urls import path

from . import views

urlpatterns = [
    path('new-cloud-capacity/', views.CloudCapacityEditorFormView.as_view(), name='new_cloud_capacity'),
    path('new-cloud-capacity/<field_format>/', views.CloudCapacityEditorFormView.as_view(), name='new_cloud_capacity'),
    path('new-edge-capacity/', views.EdgeCapacityEditorFormView.as_view(), name='new_edge_capacity'),
    path('new-edge-capacity/<field_format>/', views.EdgeCapacityEditorFormView.as_view(), name='new_edge_capacity'),
]