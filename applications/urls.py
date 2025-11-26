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
        "applications/<resource_id>/edit/",
        views.ApplicationEditorProcessFormView.as_view(),
        name="application_editor",
    ),
    path(
        "applications/<resource_id>/overview/",
        views.ApplicationEditorOverviewTemplateView.as_view(),
        name="application_overview",
    ),
    path(
        "new-application/",
        views.ApplicationEditorStartFormView.as_view(),
        name="new_application",
    ),
]
