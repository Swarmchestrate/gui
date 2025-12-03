from django.urls import path

from . import views

app_name = "application_colocations"

urlpatterns = [
    path(
        "application-colocations/",
        views.ApplicationColocationListFormView.as_view(),
        name="application_colocation_list",
    ),
    path(
        "application-colocations/new/",
        views.NewApplicationColocationFormView.as_view(),
        name="new_application_colocation",
    ),
    path(
        "application-colocations/deletes/",
        views.MultiApplicationColocationDeletionFormView.as_view(),
        name="delete_application_colocations",
    ),
    path(
        "application-colocations/<resource_id>/edit/",
        views.ApplicationColocationUpdateFormView.as_view(),
        name="update_application_colocation",
    ),
    path(
        "application-colocations/<resource_id>/delete/",
        views.ApplicationColocationDeletionFormView.as_view(),
        name="delete_application_colocation",
    ),
]
