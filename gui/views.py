from django.shortcuts import render
from django.views.generic import FormView

from .forms import NewCapacityForm


def index(request):
    return render(request, 'index.html', {
        'title': 'Home',
    })


class CapacityEditorFormView(FormView):
    template_name = 'new_capacity.html'
    form_class = NewCapacityForm

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'New Capacity',
        }) 
        return context
    