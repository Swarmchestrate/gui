from django.urls import reverse_lazy

from .tosca import generate_application_description_template

from editor.foreign_key_views import (
    OneToManyFieldEditorSectionView,
    OneToOneFieldEditorSectionView,
)
from editor.views import (
    EditorOverviewTemplateView,
    EditorStartFormView,
    EditorView,
    UpdateResourceByCategoryView,
)
from postgrest.table_names import TableNames
from resource_management.views import (
    MultiResourceDeletionFormView,
    ResourceDeletionFormView,
    ResourceListFormView,
    ToscaTemplateDownloadView,
)


class ApplicationViewMixin:
    editor_reverse_base = "applications:application_editor"
    editor_one_to_one_section_reverse_base = "applications:application_editor_one_to_one_section"
    editor_one_to_many_section_reverse_base = "applications:application_editor_one_to_many_section"
    editor_start_reverse_base = "applications:new_application"
    editor_overview_reverse_base = "applications:application_overview"
    resource_list_reverse = "applications:application_list"
    new_resource_reverse = "applications:new_application"
    resource_deletion_reverse = "applications:delete_application"
    multi_resource_deletion_reverse = "applications:delete_applications"
    tosca_template_download_reverse_base = "applications:adt_download"
    resource_type = "application"


class ApplicationEditorView(ApplicationViewMixin, EditorView):
    template_name = "applications/application_editor.html"
    table_name = TableNames.APPLICATION_NEW
    column_metadata_table_name = TableNames.APPLICATION
    editor_form_reverse = "applications:update_application_by_category"


class ApplicationOneToOneFieldEditorSectionView(ApplicationViewMixin, OneToOneFieldEditorSectionView):
    table_name = TableNames.APPLICATION_NEW
    new_one_to_one_relation_reverse_base = "applications:new_application_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "applications:update_application_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "applications:delete_application_one_to_one_relation"


class ApplicationOneToManyFieldEditorSectionView(ApplicationViewMixin, OneToManyFieldEditorSectionView):
    table_name = TableNames.APPLICATION_NEW
    possible_fk_table_column_name = "application_id"
    new_one_to_many_relation_reverse_base = "applications:new_application_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "applications:update_application_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "applications:delete_application_one_to_many_relation"


class UpdateApplicationByCategoryView(
        ApplicationViewMixin,
        UpdateResourceByCategoryView):
    table_name = TableNames.APPLICATION_NEW
    column_metadata_table_name = TableNames.APPLICATION


class ApplicationEditorStartFormView(ApplicationViewMixin, EditorStartFormView):
    template_name = "applications/new_application_start.html"
    table_name = TableNames.APPLICATION_NEW
    column_metadata_table_name = TableNames.APPLICATION
    success_url = reverse_lazy("applications:new_application")


class ApplicationDeletionFormView(ApplicationViewMixin, ResourceDeletionFormView):
    template_name = "applications/applications.html"
    success_url = reverse_lazy("applications:application_list")
    table_name = TableNames.APPLICATION_NEW


class MultiApplicationDeletionFormView(
        ApplicationViewMixin,
        MultiResourceDeletionFormView):
    template_name = "applications/applications.html"
    success_url = reverse_lazy("applications:application_list")
    table_name = TableNames.APPLICATION_NEW


class ApplicationListFormView(ApplicationViewMixin, ResourceListFormView):
    template_name = "applications/applications.html"
    table_name = TableNames.APPLICATION_NEW


class ApplicationEditorOverviewTemplateView(
        ApplicationViewMixin,
        EditorOverviewTemplateView):
    template_name = "applications/application_overview.html"
    table_name = TableNames.APPLICATION_NEW
    column_metadata_table_name = TableNames.APPLICATION


class ApplicationDescriptionTemplateDownloadView(
        ApplicationViewMixin,
        ToscaTemplateDownloadView):
    table_name = TableNames.APPLICATION_NEW

    def generate_tosca_template(self):
        return generate_application_description_template(self.resource_id)
