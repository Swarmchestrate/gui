from django.urls import path

from . import views


app_name = 'instance_types'

urlpatterns = [
    path('instance-types/', views.InstanceTypeRegistrationsListFormView.as_view(), name='instance_types_list'),
    path('instance-types/<registration_id>/edit/', views.InstanceTypeEditorProcessFormView.as_view(), name='instance_type_editor'),
    path('instance-types/<registration_id>/overview/', views.InstanceTypeEditorOverviewTemplateView.as_view(), name='instance_type_overview'),
    path('new-instance-type/', views.InstanceTypeEditorStartFormView.as_view(), name='new_instance_type'),
]
