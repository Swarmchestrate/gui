import json
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from http import HTTPStatus

from .forms import NewCapacityForm


def index(request):
    return render(request, 'index.html', {
        'title': 'Home',
    })


class CapacityEditorFormView(FormView):
    template_name = 'new_capacity.html'
    form_class = NewCapacityForm
    success_url = reverse_lazy('new_capacity')
    
    def form_invalid(self, form):
        if self.request.GET.get('response_format') == 'json':
            return JsonResponse(
                {
                    'feedback': json.loads(form.errors.as_json()),
                    'url': self.request.path,
                },
                status=HTTPStatus.BAD_REQUEST
            )
        return super().form_invalid(form)
    
    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'New Capacity',
        }) 
        return context
    