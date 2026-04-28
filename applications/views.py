from django.urls import reverse_lazy

from editor.new_foreign_key_views import (
    DeleteOneToManyRelationFormView,
    DeleteOneToOneRelationFormView,
    NewOneToManyRelationFormView,
    NewOneToOneRelationFormView,
    UpdateOneToManyRelationFormView,
    UpdateOneToOneRelationFormView,
)
from editor.new_views import (
    EditorOverviewTemplateView,
    EditorSkeletonLoaderView,
    EditorStartFormView,
    EditorTableOfContentsSectionView,
    EditorTabSectionView,
    UpdateResourceByCategoryView,
)
from postgrest.api_clients import (
    ApplicationApiClient,
    ApplicationColumnMetadataApiClient,
)
from resource_management.views import (
    MultiResourceDeletionFormView,
    ResourceDeletionFormView,
    ResourceListFormView,
)

from .utils import application_type_readable, application_type_readable_plural


class ApplicationViewMixin:
    api_client_class = ApplicationApiClient
    editor_reverse_base = "applications:application_editor"
    editor_start_reverse_base = "applications:new_application"
    editor_overview_reverse_base = "applications:application_overview"
    column_metadata_api_client_class = ApplicationColumnMetadataApiClient
    resource_list_reverse = "applications:application_list"
    new_resource_reverse = "applications:new_application"
    resource_deletion_reverse = "applications:delete_application"
    multi_resource_deletion_reverse = "applications:delete_applications"
    resource_type_readable = application_type_readable()
    resource_type_readable_plural = application_type_readable_plural()


class ApplicationEditorSkeletonLoaderView(ApplicationViewMixin, EditorSkeletonLoaderView):
    table_name = "application_new"
    template_name = "applications/application_editor.html"
    success_url = reverse_lazy("applications:new_application")
    toc_url = reverse_lazy("applications:application_editor_toc")
    tabbed_form_reverse = "applications:application_editor_tabbed_form"


class ApplicationEditorTableOfContentsView(EditorTableOfContentsSectionView):
    table_name = "application_new"
    column_metadata_table_name = "application"


class ApplicationEditorTabSectionView(EditorTabSectionView):
    table_name = "application_new"
    column_metadata_table_name = "application"
    editor_form_reverse = "applications:update_application_by_category"
    new_one_to_one_relation_reverse_base = "applications:new_application_one_to_one_relation"
    update_one_to_one_relation_reverse_base = "applications:update_application_one_to_one_relation"
    delete_one_to_one_relation_reverse_base = "applications:delete_application_one_to_one_relation"
    new_one_to_many_relation_reverse_base = "applications:new_application_one_to_many_relation"
    update_one_to_many_relation_reverse_base = "applications:update_application_one_to_many_relation"
    delete_one_to_many_relation_reverse_base = "applications:delete_application_one_to_many_relation"


class UpdateApplicationByCategoryView(
        ApplicationViewMixin,
        UpdateResourceByCategoryView):
    table_name = "application_new"
    column_metadata_table_name = "application"


class ApplicationEditorStartFormView(ApplicationViewMixin, EditorStartFormView):
    template_name = "applications/new_application_start.html"
    table_name = "application_new"
    column_metadata_table_name = "application"
    success_url = reverse_lazy("applications:new_application")


class ApplicationDeletionFormView(ApplicationViewMixin, ResourceDeletionFormView):
    template_name = "applications/applications.html"
    success_url = reverse_lazy("applications:application_list")


class MultiApplicationDeletionFormView(
        ApplicationViewMixin,
        MultiResourceDeletionFormView):
    template_name = "applications/applications.html"
    success_url = reverse_lazy("applications:application_list")


class ApplicationListFormView(ApplicationViewMixin, ResourceListFormView):
    template_name = "applications/applications.html"
    table_name = "application_new"


class ApplicationEditorOverviewTemplateView(
        ApplicationViewMixin,
        EditorOverviewTemplateView):
    template_name = "applications/application_overview.html"


class ApplicationNewOneToOneRelationFormView(
        ApplicationViewMixin,
        NewOneToOneRelationFormView):
    template_name = "applications/application_editor.html"
    table_name = "application_new"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "applications:application_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class ApplicationUpdateOneToOneRelationFormView(
        ApplicationViewMixin,
        UpdateOneToOneRelationFormView):
    template_name = "applications/application_editor.html"
    table_name = "application_new"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "applications:application_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class ApplicationDeleteOneToOneRelationFormView(
        ApplicationViewMixin,
        DeleteOneToOneRelationFormView):
    template_name = "applications/application_editor.html"
    table_name = "application_new"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "applications:application_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class ApplicationNewOneToManyRelationFormView(
        ApplicationViewMixin,
        NewOneToManyRelationFormView):
    template_name = "applications/application_editor.html"
    table_name = "application_new"
    possible_fk_table_column_name = "application_id"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "applications:application_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class ApplicationUpdateOneToManyRelationFormView(
        ApplicationViewMixin,
        UpdateOneToManyRelationFormView):
    template_name = "applications/application_editor.html"
    table_name = "application_new"
    possible_fk_table_column_name = "application_id"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "applications:application_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class ApplicationDeleteOneToManyRelationFormView(
        ApplicationViewMixin,
        DeleteOneToManyRelationFormView):
    template_name = "applications/application_editor.html"
    table_name = "application_new"
    possible_fk_table_column_name = "application_id"

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "applications:application_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)
