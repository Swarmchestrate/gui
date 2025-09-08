from django.urls import path

from . import views


app_name = 'applications'

urlpatterns = [
    path('new-application/', views.ApplicationEditorStartFormView.as_view(), name='new_application'),
    path('new-application/<registration_id>/<field_format>/', views.ApplicationEditorFormView.as_view(), name='new_application'),
]