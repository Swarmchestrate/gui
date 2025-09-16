from django.urls import reverse_lazy
from django.views.generic import FormView

from .api_endpoint_client import (
    CloudCapacityApiEndpointClient,
    EdgeCapacityApiEndpointClient,
)
from .forms import (
    CloudCapacityRegistrationForm,
    CloudCapacityEditorForm,
    EdgeCapacityEditorForm,
    EdgeCapacityRegistrationForm,
)

from editor.views import (
    EditorView,
    EditorFormView,
    EditorStartFormView,
    RegistrationsListFormView,
)


# Cloud Capacity
class CloudCapacityEditorView(EditorView):
    editor_registration_list_url_reverse = 'capacities:cloud_capacities_list'
    editor_url_reverse_base = 'capacities:cloud_capacity_editor'
    editor_start_url_reverse_base = 'capacities:new_cloud_capacity'
    registration_type_name_singular = 'cloud capacity'
    registration_type_name_plural = 'cloud capacities'
    api_endpoint_client_class = CloudCapacityApiEndpointClient


class CloudCapacityEditorStartFormView(CloudCapacityEditorView, EditorStartFormView, FormView):
    template_name = 'capacities/new_cloud_capacity_start.html'
    form_class = CloudCapacityRegistrationForm


class CloudCapacityEditorFormView(CloudCapacityEditorView, EditorFormView):
    template_name = 'capacities/new_cloud_capacity.html'
    form_class = CloudCapacityEditorForm
    success_url = reverse_lazy('capacities:new_cloud_capacity')


class CloudCapacityRegistrationsListFormView(CloudCapacityEditorView, RegistrationsListFormView):
    new_registration_reverse = 'capacities:new_cloud_capacity'


# Edge Capacity
class EdgeCapacityEditorView(EditorView):
    editor_registration_list_url_reverse = 'capacities:edge_capacities_list'
    editor_url_reverse_base = 'capacities:edge_capacity_editor'
    editor_start_url_reverse_base = 'capacities:new_edge_capacity'
    registration_type_name_singular = 'edge capacity'
    registration_type_name_plural = 'edge capacities'
    title_base = 'New Edge Capacity'
    api_endpoint_client_class = EdgeCapacityApiEndpointClient


class EdgeCapacityEditorStartFormView(EdgeCapacityEditorView, EditorStartFormView):
    template_name = 'capacities/new_edge_capacity_start.html'
    form_class = EdgeCapacityRegistrationForm


class EdgeCapacityEditorFormView(EdgeCapacityEditorView, EditorFormView):
    template_name = 'capacities/new_edge_capacity.html'
    form_class = EdgeCapacityEditorForm
    success_url = reverse_lazy('capacities:new_edge_capacity')


class EdgeCapacityRegistrationsListFormView(EdgeCapacityEditorView, RegistrationsListFormView):
    new_registration_reverse = 'capacities:new_edge_capacity'
