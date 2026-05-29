from django.urls import path

from . import foreign_key_views

app_name = "editor"

urlpatterns = [
    path(
        "<table_name>/<resource_id>/one-to-many-field/<fk_table_name>/",
        foreign_key_views.OneToManyFieldEditorSectionView.as_view(),
        name="one_to_many_field_section",
    ),
]
