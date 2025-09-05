from django.urls import reverse_lazy
from django.views.generic import FormView

from .api_endpoint_client import CapacityApiEndpointClient
from .forms import (
    CloudCapacityRegistrationForm,
    CloudCapacityEditorForm,
    EdgeCapacityEditorForm,
    EdgeCapacityRegistrationForm,
)

from editor.views import (
    EditorView,
    EditorFormView,
    EditorStartFormView
)


# Cloud Capacity
class CloudCapacityEditorView(EditorView):
    title_base = 'New Cloud Capacity'
    api_endpoint_client_class = CapacityApiEndpointClient


class CloudCapacityEditorStartFormView(CloudCapacityEditorView, EditorStartFormView, FormView):
    template_name = 'capacities/new_cloud_capacity_start.html'
    form_class = CloudCapacityRegistrationForm
    success_url = reverse_lazy('capacities:new_cloud_capacity')


class CloudCapacityEditorFormView(CloudCapacityEditorView, EditorFormView):
    template_name = 'capacities/new_cloud_capacity.html'
    form_class = CloudCapacityEditorForm
    success_url = reverse_lazy('capacities:new_cloud_capacity')


# Edge Capacity
class EdgeCapacityEditorView(EditorView):
    title_base = 'New Edge Capacity'
    api_endpoint_client_class = CapacityApiEndpointClient


class EdgeCapacityEditorStartFormView(EdgeCapacityEditorView, EditorStartFormView):
    template_name = 'capacities/new_edge_capacity_start.html'
    form_class = EdgeCapacityRegistrationForm
    success_url = reverse_lazy('capacities:new_edge_capacity')


class EdgeCapacityEditorFormView(EdgeCapacityEditorView, EditorFormView):
    template_name = 'capacities/new_edge_capacity.html'
    form_class = EdgeCapacityEditorForm
    success_url = reverse_lazy('capacities:new_edge_capacity')
