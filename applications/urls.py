from django.urls import path

from . import views

app_name = "applications"

urlpatterns = [
    path(
        "applications/",
        views.ApplicationListFormView.as_view(),
        name="application_list",
    ),
    path(
        "applications/new/",
        views.ApplicationEditorStartFormView.as_view(),
        name="new_application",
    ),
    path(
        "applications/deletes/",
        views.MultiApplicationDeletionFormView.as_view(),
        name="delete_applications",
    ),
    path(
        "applications/<resource_id>/overview/",
        views.ApplicationEditorOverviewTemplateView.as_view(),
        name="application_overview",
    ),
    path(
        "applications/<resource_id>/edit/",
        views.ApplicationEditorProcessFormView.as_view(),
        name="application_editor",
    ),
]
