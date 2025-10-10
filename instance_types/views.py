from django.urls import reverse_lazy

from .api_endpoint_client import InstanceTypeApiEndpointClient, InstanceTypeColumnMetadataApiEndpointClient
from .forms import InstanceTypeEditorForm, InstanceTypeRegistrationForm

from editor.views import (
    EditorView,
    EditorProcessFormView,
    EditorOverviewTemplateView,
    EditorStartFormView,
    RegistrationsListFormView,
)


class InstanceTypeEditorView(EditorView):
    editor_registration_list_url_reverse = 'instance_types:instance_types_list'
    editor_url_reverse_base = 'instance_types:instance_type_editor'
    editor_start_url_reverse_base = 'instance_types:new_instance_type'
    editor_overview_url_reverse_base = 'instance_types:instance_type_overview'
    registration_type_name_singular = 'instance type'
    registration_type_name_plural = 'instance types'
    api_endpoint_client_class = InstanceTypeApiEndpointClient
    column_metadata_api_endpoint_client_class = InstanceTypeColumnMetadataApiEndpointClient


class InstanceTypeEditorStartFormView(InstanceTypeEditorView, EditorStartFormView):
    template_name = 'instance_types/new_instance_type_start.html'
    form_class = InstanceTypeRegistrationForm
    success_url = reverse_lazy('instance_types:new_instance_type')


class InstanceTypeEditorProcessFormView(InstanceTypeEditorView, EditorProcessFormView):
    template_name = 'instance_types/instance_type_editor.html'
    main_form_class = InstanceTypeEditorForm
    success_url = reverse_lazy('instance_types:new_instance_type')


class InstanceTypeRegistrationsListFormView(InstanceTypeEditorView, RegistrationsListFormView):
    new_registration_reverse = 'instance_types:new_instance_type'


class InstanceTypeEditorOverviewTemplateView(InstanceTypeEditorView, EditorOverviewTemplateView):
    pass
