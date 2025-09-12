from django.urls import reverse_lazy

from .api_endpoint_client import ApplicationApiEndpointClient
from .forms import ApplicationEditorForm, ApplicationRegistrationForm

from editor.views import (
    EditorView,
    EditorFormView,
    EditorStartFormView,
    RegistrationsTemplateView,
)


class ApplicationEditorView(EditorView):
    editor_registration_list_url_reverse = 'applications:applications_list'
    editor_url_reverse_base = 'applications:application_editor'
    editor_start_url_reverse_base = 'applications:new_application'
    registration_type_name_singular = 'application'
    registration_type_name_plural = 'applications'
    api_endpoint_client_class = ApplicationApiEndpointClient


class ApplicationEditorStartFormView(ApplicationEditorView, EditorStartFormView):
    template_name = 'applications/new_application_start.html'
    form_class = ApplicationRegistrationForm
    success_url = reverse_lazy('applications:new_application')


class ApplicationEditorFormView(ApplicationEditorView, EditorFormView):
    template_name = 'applications/new_application.html'
    form_class = ApplicationEditorForm
    success_url = reverse_lazy('applications:new_application')


class ApplicationRegistrationsTemplateView(ApplicationEditorView, RegistrationsTemplateView):
    pass
