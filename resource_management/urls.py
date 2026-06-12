from django.urls import path

from . import views

app_name = "resource_management"

urlpatterns = [
    path(
        "column-metadata/",
        views.ColumnMetadataManagementView.as_view(),
        name="manage_column_metadata",
    ),
    path(
        "column-metadata/new/",
        views.NewColumnMetadataFormView.as_view(),
        name="new_column_metadata",
    ),
    path(
        "column-metadata/deletes/",
        views.MultiColumnMetadataDeletionFormView.as_view(),
        name="delete_column_metadata_multi",
    ),
    path(
        "column-metadata/<resource_id>/delete/",
        views.ColumnMetadataDeletionFormView.as_view(),
        name="delete_column_metadata",
    ),
    path(
        "column-metadata/<resource_id>/update/",
        views.UpdateColumnMetadataFormView.as_view(),
        name="update_column_metadata",
    ),
]
