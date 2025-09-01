from django.urls import reverse_lazy

from .forms import NewApplicationForm

from editor.views import EditorFormView


class ApplicationEditorFormView(EditorFormView):
    template_name = 'applications/new_application.html'
    form_class = NewApplicationForm
    success_url = reverse_lazy('new_application')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'New Application',
        }) 
        return context