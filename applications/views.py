from django.urls import reverse_lazy

from editor.base_views import (
    EditorOverviewTemplateView,
    EditorProcessFormView,
    EditorStartFormView,
    EditorView,
    ResourceListFormView,
)

from .api.api_clients import (
    ApplicationApiClient,
    ApplicationColumnMetadataApiClient,
)
from .forms import ApplicationEditorForm, ApplicationRegistrationForm


class ApplicationEditorView(EditorView):
    editor_resource_list_url_reverse = "applications:applications_list"
    editor_url_reverse_base = "applications:application_editor"
    editor_start_url_reverse_base = "applications:new_application"
    editor_overview_url_reverse_base = "applications:application_overview"
    resource_type_name_singular = "application"
    resource_type_name_plural = "applications"
    api_client_class = ApplicationApiClient
    column_metadata_api_client_class = ApplicationColumnMetadataApiClient


class ApplicationEditorStartFormView(ApplicationEditorView, EditorStartFormView):
    template_name = "applications/new_application_start.html"
    form_class = ApplicationRegistrationForm
    success_url = reverse_lazy("applications:new_application")


class ApplicationEditorProcessFormView(ApplicationEditorView, EditorProcessFormView):
    template_name = "applications/application_editor.html"
    main_form_class = ApplicationEditorForm
    success_url = reverse_lazy("applications:new_application")


class ApplicationListFormView(ApplicationEditorView, ResourceListFormView):
    template_name = "applications/applications.html"
    new_resource_reverse = "applications:new_application"


class ApplicationEditorOverviewTemplateView(
    ApplicationEditorView, EditorOverviewTemplateView
):
    template_name = "applications/application_overview.html"
