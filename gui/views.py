import json
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from http import HTTPStatus

from .forms import (
    NewApplicationForm,
    NewCapacityForm,
    NewCloudCapacityForm,
    NewEdgeCapacityForm,
)


def index(request):
    return render(request, 'index.html', {
        'title': 'Home',
    })


class EditorFormView(FormView):
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


class CapacityEditorFormView(EditorFormView):
    template_name = 'new_capacity.html'
    form_class = NewCapacityForm
    success_url = reverse_lazy('new_capacity')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'New Capacity',
        }) 
        return context


class CloudCapacityEditorFormView(EditorFormView):
    template_name = 'new_cloud_capacity.html'
    form_class = NewCloudCapacityForm
    success_url = reverse_lazy('new_cloud_capacity')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'New Cloud Capacity',
        }) 
        return context


class EdgeCapacityEditorFormView(EditorFormView):
    template_name = 'new_edge_capacity.html'
    form_class = NewEdgeCapacityForm
    success_url = reverse_lazy('new_edge_capacity')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'New Edge Capacity',
        }) 
        return context


class ApplicationEditorFormView(EditorFormView):
    template_name = 'new_application.html'
    form_class = NewApplicationForm
    success_url = reverse_lazy('new_application')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'New Application',
        }) 
        return context