from django.urls import path

from . import views


app_name = 'applications'

urlpatterns = [
    path('applications/', views.ApplicationRegistrationsListFormView.as_view(), name='applications_list'),
    path('applications/<registration_id>/edit/', views.ApplicationEditorFormView.as_view(), name='application_editor'),
    path('new-application/', views.ApplicationEditorStartFormView.as_view(), name='new_application'),
]
