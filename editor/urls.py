from django.urls import path

from . import foreign_key_field_views

app_name = "editor"

urlpatterns = [
    path(
        "foreign-key-editor/<table_name>/<resource_id>/one-to-one-field/<fk_column_name>/",
        foreign_key_field_views.OneToOneFieldPopupSectionView.as_view(),
        name="one_to_one_field_popup_section",
    ),
    path(
        "foreign-key-editor/<table_name>/<resource_id>/one-to-many-field/<fk_table_name>/",
        foreign_key_field_views.OneToManyFieldPopupSectionView.as_view(),
        name="one_to_many_field_popup_section",
    ),
]
