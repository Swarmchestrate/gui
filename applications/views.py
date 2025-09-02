from django.urls import reverse_lazy

from .api_client import ApplicationApiClient
from .forms import NewApplicationForm

from editor.views import EditorFormView


class ApplicationEditorFormView(EditorFormView):
    template_name = 'applications/new_application.html'
    form_class = NewApplicationForm
    success_url = reverse_lazy('new_application')

    api_client_class = ApplicationApiClient

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'New Application',
        }) 
        return context