from django.urls import path

from . import views

app_name = "resource_management"

urlpatterns = [
    path(
        "column-metadata/",
        views.ColumnMetadataManagementListView.as_view(),
        name="manage_column_metadata",
    ),
    path(
        "column-metadata/table/<table_name>/",
        views.ColumnMetadataManagementForTableView.as_view(),
        name="manage_column_metadata_for_table",
    ),
    path(
        "column-metadata/table/<table_name>/category-order/update/",
        views.CategoryOrderFormView.as_view(),
        name="update_category_order",
    ),
    path(
        "column-metadata/new/table/<table_name>/column/<column_name>/",
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
