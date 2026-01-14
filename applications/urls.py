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
        views.ApplicationEditorBaseTemplateView.as_view(),
        name="application_editor",
    ),
    path(
        "applications/<resource_id>/delete/",
        views.ApplicationDeletionFormView.as_view(),
        name="delete_application",
    ),
    path(
        "applications/<resource_id>/one-to-one-column/<fk_column_name>/new/",
        views.ApplicationNewOneToOneRelationFormView.as_view(),
        name="new_application_one_to_one_relation",
    ),
    path(
        "applications/<resource_id>/one-to-one-column/<fk_column_name>/",
        views.ApplicationUpdateOneToOneRelationFormView.as_view(),
        name="update_application_one_to_one_relation",
    ),
    path(
        "applications/<resource_id>/one-to-one-column/<fk_column_name>/delete/",
        views.ApplicationDeleteOneToOneRelationFormView.as_view(),
        name="delete_application_one_to_one_relation",
    ),
    path(
        "applications/<resource_id>/one-to-many-column/<fk_column_name>/new/",
        views.ApplicationNewOneToManyRelationFormView.as_view(),
        name="new_application_one_to_many_relation",
    ),
    path(
        "applications/<resource_id>/one-to-many-column/<fk_column_name>/<fk_resource_id>/",
        views.ApplicationUpdateOneToManyRelationFormView.as_view(),
        name="update_application_one_to_many_relation",
    ),
    path(
        "applications/<resource_id>/one-to-many-column/<fk_column_name>/<fk_resource_id>/delete/",
        views.ApplicationDeleteOneToManyRelationFormView.as_view(),
        name="delete_application_one_to_many_relation",
    ),
]
