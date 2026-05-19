from .views import ApplicationViewMixin

from editor.foreign_key_views_new import (
    DialogBasedOneToManyFieldView,
    DialogBasedOneToOneFieldView,
    EditorBasedOneToManyFieldView,
    EditorBasedOneToOneFieldView,
    EditorForeignKeyFieldView,
)
from postgrest.table_names import TableNames

class ApplicationDialogBasedOneToOneFieldView(ApplicationViewMixin, DialogBasedOneToOneFieldView):
    table_name = TableNames.APPLICATION_NEW
    new_one_to_one_relation_reverse_base = "applications:new_application_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "applications:update_application_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "applications:delete_application_one_to_one_relation"


class ApplicationDialogBasedOneToManyFieldView(ApplicationViewMixin, DialogBasedOneToManyFieldView):
    table_name = TableNames.APPLICATION_NEW
    possible_fk_table_column_name = "application_id"
    new_one_to_many_relation_reverse_base = "applications:new_application_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "applications:update_application_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "applications:delete_application_one_to_many_relation"


class ApplicationEditorBasedOneToOneFieldView(ApplicationViewMixin, EditorBasedOneToOneFieldView):
    view_class = ApplicationDialogBasedOneToOneFieldView
    table_name = TableNames.APPLICATION_NEW
    new_one_to_one_relation_reverse_base = "applications:new_application_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "applications:update_application_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "applications:delete_application_one_to_one_relation"


class ApplicationEditorBasedOneToManyFieldView(ApplicationViewMixin, EditorBasedOneToManyFieldView):
    view_class = ApplicationDialogBasedOneToManyFieldView
    table_name = TableNames.APPLICATION_NEW
    possible_fk_table_column_name = "application_id"
    new_one_to_many_relation_reverse_base = "applications:new_application_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "applications:update_application_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "applications:delete_application_one_to_many_relation"


class ApplicationEditorForeignKeyFieldView(
        ApplicationViewMixin,
        EditorForeignKeyFieldView):
    table_name = TableNames.APPLICATION_NEW
    dialog_based_one_to_one_field_view_class = ApplicationDialogBasedOneToOneFieldView
    dialog_based_one_to_many_field_view_class = ApplicationDialogBasedOneToManyFieldView
    editor_based_one_to_one_field_view_class = ApplicationEditorBasedOneToOneFieldView
    editor_based_one_to_many_field_view_class = ApplicationEditorBasedOneToManyFieldView