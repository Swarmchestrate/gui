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
        "applications/api/<resource_id>/editor/one-to-one-section/<fk_column_name>/",
        views.ApplicationOneToOneFieldEditorSectionView.as_view(),
        name="application_editor_one_to_one_section",
    ),
    path(
        "applications/api/<resource_id>/editor/one-to-many-section/<fk_table_name>/",
        views.ApplicationOneToManyFieldEditorSectionView.as_view(),
        name="application_editor_one_to_many_section",
    ),
    path(
        "applications/api/<resource_id>/editor/one-to-one-section/non-dialog-based/<fk_column_name>/",
        views.ApplicationOneToOneFieldEditorSectionView.as_view(),
        name="application_editor_non_dialog_based_one_to_one_section",
    ),
    path(
        "applications/api/<resource_id>/editor/one-to-many-section/non-dialog-based/<fk_table_name>/",
        views.ApplicationOneToManyFieldEditorSectionView.as_view(),
        name="application_editor_non_dialog_based_one_to_many_section",
    ),
    path(
        "applications/api/<resource_id>/edit/",
        views.UpdateApplicationByCategoryView.as_view(),
        name="update_application_by_category",
    ),
    path(
        "applications/<resource_id>/overview/",
        views.ApplicationEditorOverviewTemplateView.as_view(),
        name="application_overview",
    ),
    path(
        "applications/<resource_id>/edit/",
        views.ApplicationEditorView.as_view(),
        name="application_editor",
    ),
    path(
        "applications/<resource_id>/delete/",
        views.ApplicationDeletionFormView.as_view(),
        name="delete_application",
    ),
    path(
        "applications/<resource_id>/download/",
        views.ApplicationDescriptionTemplateDownloadView.as_view(),
        name="adt_download",
    ),
]
