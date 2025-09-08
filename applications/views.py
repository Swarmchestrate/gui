from django.urls import reverse_lazy

from .api_endpoint_client import ApplicationApiEndpointClient
from .forms import ApplicationEditorForm, ApplicationRegistrationForm

from editor.views import (
    EditorView,
    EditorFormView,
    EditorStartFormView
)


class ApplicationEditorView(EditorView):
    editor_type = 'application'
    title_base = 'New Application'
    api_endpoint_client_class = ApplicationApiEndpointClient


class ApplicationEditorStartFormView(ApplicationEditorView, EditorStartFormView):
    template_name = 'applications/new_application_start.html'
    form_class = ApplicationRegistrationForm
    success_url = reverse_lazy('applications:new_application')


class ApplicationEditorFormView(ApplicationEditorView, EditorFormView):
    template_name = 'applications/new_application.html'
    form_class = ApplicationEditorForm
    success_url = reverse_lazy('applications:new_application')