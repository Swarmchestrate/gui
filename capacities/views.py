from django.urls import reverse_lazy
from django.views.generic import FormView

from .api_client import CapacityApiClient
from .forms import (
    CloudCapacityRegistrationForm,
    CloudCapacityEditorForm,
    EdgeCapacityEditorForm,
)

from editor.views import (
    EditorView,
    EditorFormView,
    EditorStartTemplateView
)


# Cloud Capacity
class CloudCapacityEditorView(EditorView):
    title_base = 'New Cloud Capacity'
    api_client_class = CapacityApiClient


class CloudCapacityEditorStartTemplateView(CloudCapacityEditorView, EditorStartTemplateView, FormView):
    template_name = 'capacities/new_cloud_capacity_start.html'
    form_class = CloudCapacityRegistrationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'api_client': self.api_client_class(),
            'field_names': [],
        })
        return kwargs


class CloudCapacityEditorFormView(CloudCapacityEditorView, EditorFormView):
    template_name = 'capacities/new_cloud_capacity.html'
    form_class = CloudCapacityEditorForm
    success_url = reverse_lazy('new_cloud_capacity')


# Edge Capacity
class EdgeCapacityEditorView(EditorView):
    title_base = 'New Edge Capacity'
    api_client_class = CapacityApiClient


class EdgeCapacityEditorStartTemplateView(EdgeCapacityEditorView, EditorStartTemplateView):
    template_name = 'capacities/new_edge_capacity_start.html'


class EdgeCapacityEditorFormView(EdgeCapacityEditorView, EditorFormView):
    template_name = 'capacities/new_edge_capacity.html'
    form_class = EdgeCapacityEditorForm
    success_url = reverse_lazy('new_edge_capacity')
