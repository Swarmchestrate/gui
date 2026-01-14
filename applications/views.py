from django.urls import reverse_lazy

from editor.base_views import (
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    EditorContextMixin,
    ResourceTypeNameContextMixin,
)
from editor.views import (
    DeleteOneToManyRelationFormView,
    DeleteOneToOneRelationFormView,
    EditorBaseTemplateView,
    EditorCategoryBasedFormView,
    EditorEnabledTabListTemplateView,
    EditorFormView,
    EditorOverviewTemplateView,
    EditorStartFormView,
    EditorTabbedFormTemplateView,
    NewOneToManyRelationFormView,
    NewOneToOneRelationFormView,
    UpdateOneToManyRelationFormView,
    UpdateOneToOneRelationFormView,
)

# from postgrest.mocks.mock_api_clients import (
#     MockApplicationApiClient as ApplicationApiClient,
# )
# from postgrest.mocks.mock_api_clients import (
#     MockApplicationColumnMetadataApiClient as ApplicationColumnMetadataApiClient,
# )
from postgrest.api_clients import (
    ApplicationApiClient,
    ApplicationColumnMetadataApiClient,
)
from resource_management.views import (
    MultiResourceDeletionFormView,
    ResourceDeletionFormView,
    ResourceListContextMixin,
    ResourceListFormView,
)

from .forms import (
    ApplicationCategoryBasedEditorForm,
    ApplicationEditorForm,
    ApplicationRegistrationForm,
)
from .utils import application_type_readable, application_type_readable_plural


class ApplicationViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    EditorContextMixin,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = ApplicationApiClient
    editor_reverse_base = "applications:update_application_by_category"
    editor_start_reverse_base = "applications:new_application"
    editor_overview_reverse_base = "applications:application_overview"
    column_metadata_api_client_class = ApplicationColumnMetadataApiClient
    resource_list_reverse = "applications:application_list"
    new_resource_reverse = "applications:new_application"
    resource_deletion_reverse = "applications:delete_application"
    multi_resource_deletion_reverse = "applications:delete_applications"
    resource_type_readable = application_type_readable()
    resource_type_readable_plural = application_type_readable_plural()


class ApplicationEditorStartFormView(ApplicationViewMixin, EditorStartFormView):
    template_name = "applications/new_application_start.html"
    form_class = ApplicationRegistrationForm
    success_url = reverse_lazy("applications:new_application")


class ApplicationEditorEnabledTabListTemplateView(
    ApplicationViewMixin, EditorEnabledTabListTemplateView
):
    pass


class ApplicationEditorFormView(ApplicationViewMixin, EditorFormView):
    form_class = ApplicationEditorForm


class ApplicationEditorCategoryBasedFormView(
    ApplicationViewMixin, EditorCategoryBasedFormView
):
    form_class = ApplicationCategoryBasedEditorForm


class ApplicationEditorTabbedFormTemplateView(
    ApplicationViewMixin, EditorTabbedFormTemplateView
):
    form_class = ApplicationEditorForm
    editor_form_reverse = "applications:update_application_by_category"
    new_one_to_one_relation_reverse_base = (
        "applications:new_application_one_to_one_relation"
    )
    update_one_to_one_relation_reverse_base = (
        "applications:update_application_one_to_one_relation"
    )
    delete_one_to_one_relation_reverse_base = (
        "applications:delete_application_one_to_one_relation"
    )
    new_one_to_many_relation_reverse_base = (
        "applications:new_application_one_to_many_relation"
    )
    update_one_to_many_relation_reverse_base = (
        "applications:update_application_one_to_many_relation"
    )
    delete_one_to_many_relation_reverse_base = (
        "applications:delete_application_one_to_many_relation"
    )


class ApplicationEditorBaseTemplateView(ApplicationViewMixin, EditorBaseTemplateView):
    template_name = "applications/application_editor.html"
    success_url = reverse_lazy("applications:new_application")
    toc_url = reverse_lazy("applications:application_editor_toc")
    tabbed_form_reverse = "applications:application_editor_tabbed_form"


class ApplicationDeletionFormView(ApplicationViewMixin, ResourceDeletionFormView):
    template_name = "applications/applications.html"
    success_url = "applications:application_list"


class MultiApplicationDeletionFormView(
    ApplicationViewMixin, MultiResourceDeletionFormView
):
    template_name = "applications/applications.html"
    success_url = "applications:application_list"


class ApplicationListFormView(ApplicationViewMixin, ResourceListFormView):
    template_name = "applications/applications.html"


class ApplicationEditorOverviewTemplateView(
    ApplicationViewMixin, EditorOverviewTemplateView
):
    template_name = "applications/application_overview.html"


class ApplicationNewOneToOneRelationFormView(
    ApplicationViewMixin, NewOneToOneRelationFormView
):
    template_name = "applications/application_editor.html"
    api_client = ApplicationApiClient

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "applications:application_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class ApplicationUpdateOneToOneRelationFormView(
    ApplicationViewMixin, UpdateOneToOneRelationFormView
):
    template_name = "applications/application_editor.html"
    api_client = ApplicationApiClient

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "applications:application_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class ApplicationDeleteOneToOneRelationFormView(
    ApplicationViewMixin, DeleteOneToOneRelationFormView
):
    template_name = "applications/application_editor.html"
    api_client = ApplicationApiClient

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "applications:application_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class ApplicationNewOneToManyRelationFormView(
    ApplicationViewMixin, NewOneToManyRelationFormView
):
    template_name = "applications/application_editor.html"
    api_client = ApplicationApiClient

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "applications:application_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class ApplicationUpdateOneToManyRelationFormView(
    ApplicationViewMixin, UpdateOneToManyRelationFormView
):
    template_name = "applications/application_editor.html"
    api_client = ApplicationApiClient

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "applications:application_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)


class ApplicationDeleteOneToManyRelationFormView(
    ApplicationViewMixin, DeleteOneToManyRelationFormView
):
    template_name = "applications/application_editor.html"
    api_client = ApplicationApiClient

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(
            "applications:application_editor",
            kwargs={"resource_id": kwargs["resource_id"]},
        )
        return super().dispatch(request, *args, **kwargs)
