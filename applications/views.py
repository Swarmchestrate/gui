from django.urls import reverse_lazy

from editor.views import (
    EditorOverviewTemplateView,
    EditorProcessFormView,
    EditorStartFormView,
    EditorView,
    RegistrationsListFormView,
)

from .api_endpoint_client import (
    ApplicationApiEndpoint,
    ApplicationColumnMetadataApiEndpoint,
)
from .forms import ApplicationEditorForm, ApplicationRegistrationForm


class ApplicationEditorView(EditorView):
    editor_registration_list_url_reverse = "applications:applications_list"
    editor_url_reverse_base = "applications:application_editor"
    editor_start_url_reverse_base = "applications:new_application"
    editor_overview_url_reverse_base = "applications:application_overview"
    registration_type_name_singular = "application"
    registration_type_name_plural = "applications"
    api_endpoint_client_class = ApplicationApiEndpoint
    column_metadata_api_endpoint_client_class = ApplicationColumnMetadataApiEndpoint


class ApplicationEditorStartFormView(ApplicationEditorView, EditorStartFormView):
    template_name = "applications/new_application_start.html"
    form_class = ApplicationRegistrationForm
    success_url = reverse_lazy("applications:new_application")


class ApplicationEditorProcessFormView(ApplicationEditorView, EditorProcessFormView):
    template_name = "applications/application_editor.html"
    main_form_class = ApplicationEditorForm
    success_url = reverse_lazy("applications:new_application")


class ApplicationRegistrationsListFormView(
    ApplicationEditorView, RegistrationsListFormView
):
    template_name = "applications/applications.html"
    new_registration_reverse = "applications:new_application"


class ApplicationEditorOverviewTemplateView(
    ApplicationEditorView, EditorOverviewTemplateView
):
    template_name = "applications/application_overview.html"
