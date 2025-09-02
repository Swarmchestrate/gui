from django.urls import reverse_lazy

from .api_client import CapacityApiClient
from .forms import (
    NewCloudCapacityForm,
    NewEdgeCapacityForm,
)

from editor.views import EditorView, EditorFormView, EditorStartTemplateView


# Cloud Capacity
class CloudCapacityEditorView(EditorView):
    title_base = 'New Cloud Capacity'
    api_client_class = CapacityApiClient


class CloudCapacityEditorStartTemplateView(CloudCapacityEditorView, EditorStartTemplateView):
    template_name = 'capacities/new_cloud_capacity_start.html'


class CloudCapacityEditorFormView(CloudCapacityEditorView, EditorFormView):
    template_name = 'capacities/new_cloud_capacity.html'
    form_class = NewCloudCapacityForm
    success_url = reverse_lazy('new_cloud_capacity')


# Edge Capacity
class EdgeCapacityEditorView(EditorView):
    title_base = 'New Edge Capacity'
    api_client_class = CapacityApiClient


class EdgeCapacityEditorStartTemplateView(EdgeCapacityEditorView, EditorStartTemplateView):
    template_name = 'capacities/new_edge_capacity_start.html'


class EdgeCapacityEditorFormView(EdgeCapacityEditorView, EditorFormView):
    template_name = 'capacities/new_edge_capacity.html'
    form_class = NewEdgeCapacityForm
    success_url = reverse_lazy('new_edge_capacity')
