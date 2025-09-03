from django.urls import reverse_lazy

from .api_client import ApplicationApiClient
from .forms import ApplicationEditorForm, ApplicationRegistrationForm

from editor.views import (
    EditorView,
    EditorFormView,
    EditorStartFormView
)


class ApplicationEditorView(EditorView):
    title_base = 'New Application'
    api_client_class = ApplicationApiClient


class ApplicationEditorStartFormView(ApplicationEditorView, EditorStartFormView):
    template_name = 'applications/new_application_start.html'
    form_class = ApplicationRegistrationForm


class ApplicationEditorFormView(ApplicationEditorView, EditorFormView):
    template_name = 'applications/new_application.html'
    form_class = ApplicationEditorForm
    success_url = reverse_lazy('new_application')