from django.urls import path

from . import views

app_name = "postgrest"

urlpatterns = [
    path(
        "<table_name>/columns/",
        views.GetTableColumnsView.as_view(),
        name="get_table_columns"
    ),
    path(
        "<table_name>/<resource_id>/one-to-one-relation/<fk_column_name>/new/",
        views.NewOneToOneRelationFormView.as_view(),
        name="new_one_to_one_relation",
    ),
    path(
        "<table_name>/<resource_id>/one-to-one-relation/<fk_column_name>/edit/",
        views.UpdateOneToOneRelationFormView.as_view(),
        name="update_one_to_one_relation",
    ),
    path(
        "<table_name>/<resource_id>/one-to-one-relation/<fk_column_name>/delete/",
        views.DeleteOneToOneRelationFormView.as_view(),
        name="delete_one_to_one_relation",
    ),
    path(
        "<table_name>/<resource_id>/one-to-many-relation/<fk_table_name>/new/",
        views.NewOneToManyRelationFormView.as_view(),
        name="new_one_to_many_relation",
    ),
    path(
        "<table_name>/<resource_id>/one-to-many-relation/<fk_table_name>/<fk_resource_id>/edit/",
        views.UpdateOneToManyRelationFormView.as_view(),
        name="update_one_to_many_relation",
    ),
    path(
        "<table_name>/<resource_id>/one-to-many-relation/<fk_table_name>/<fk_resource_id>/delete/",
        views.DeleteOneToManyRelationFormView.as_view(),
        name="delete_one_to_many_relation",
    ),
]
