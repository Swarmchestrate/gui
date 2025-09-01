from django.urls import path

from . import views

urlpatterns = [
    path('new-application/', views.ApplicationEditorFormView.as_view(), name='new_application'),
]