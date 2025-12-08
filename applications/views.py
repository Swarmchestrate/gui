from django.urls import reverse_lazy

from editor.base_views import (
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    EditorContextMixin,
    ResourceTypeNameContextMixin,
)
from editor.views import (
    EditorOverviewTemplateView,
    EditorProcessFormView,
    EditorStartFormView,
)
from resource_management.views import (
    MultiResourceDeletionFormView,
    ResourceDeletionFormView,
    ResourceListContextMixin,
    ResourceListFormView,
)

from .api.api_clients import (
    ApplicationApiClient,
    ApplicationColumnMetadataApiClient,
)
from .forms import ApplicationEditorForm, ApplicationRegistrationForm
from .utils import application_type_readable, application_type_readable_plural


class ApplicationViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    EditorContextMixin,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
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


class ApplicationEditorStartFormView(ApplicationViewMixin, EditorStartFormView):
    template_name = "applications/new_application_start.html"
    form_class = ApplicationRegistrationForm
    success_url = reverse_lazy("applications:new_application")


class ApplicationEditorProcessFormView(ApplicationViewMixin, EditorProcessFormView):
    template_name = "applications/application_editor.html"
    form_class = ApplicationEditorForm
    success_url = reverse_lazy("applications:new_application")


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
