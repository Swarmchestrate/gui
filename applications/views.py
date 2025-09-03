from django.urls import reverse_lazy

from .api_client import ApplicationApiClient
from .forms import ApplicationEditorForm

from editor.views import EditorView, EditorFormView, EditorStartTemplateView


class ApplicationEditorView(EditorView):
    title_base = 'New Application'
    api_client_class = ApplicationApiClient


class ApplicationEditorStartTemplateView(ApplicationEditorView, EditorStartTemplateView):
    template_name = 'applications/new_application_start.html'


class ApplicationEditorFormView(ApplicationEditorView, EditorFormView):
    template_name = 'applications/new_application.html'
    form_class = ApplicationEditorForm
    success_url = reverse_lazy('new_application')