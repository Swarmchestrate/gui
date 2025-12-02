from django.urls import path

from . import views

app_name = "application_environment_vars"

urlpatterns = [
    path(
        "application-environment-vars/",
        views.ApplicationEnvironmentVarListFormView.as_view(),
        name="application_environment_var_list",
    ),
    path(
        "application-environment-vars/new/",
        views.NewApplicationEnvironmentVarFormView.as_view(),
        name="new_application_environment_var",
    ),
    path(
        "application-environment-vars/deletes/",
        views.MultiApplicationEnvironmentVarDeletionFormView.as_view(),
        name="delete_application_environment_vars",
    ),
    path(
        "application-environment-vars/<resource_id>/edit/",
        views.ApplicationEnvironmentVarUpdateFormView.as_view(),
        name="update_application_environment_var",
    ),
    path(
        "application-environment-vars/<resource_id>/delete/",
        views.ApplicationEnvironmentVarDeletionFormView.as_view(),
        name="delete_application_environment_var",
    ),
]
