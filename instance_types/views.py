from django.urls import reverse_lazy

from editor.base_views import (
    EditorOverviewTemplateView,
    EditorProcessFormView,
    EditorStartFormView,
    EditorView,
    ResourceListFormView,
)

# from .api.api_clients import (
#     InstanceTypeApiClient,
#     InstanceTypeColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    InstanceTypeApiClient,
    InstanceTypeColumnMetadataApiClient,
)
from .forms import InstanceTypeEditorForm, InstanceTypeRegistrationForm


class InstanceTypeEditorView(EditorView):
    editor_resource_list_url_reverse = "instance_types:instance_type_list"
    editor_url_reverse_base = "instance_types:instance_type_editor"
    editor_start_url_reverse_base = "instance_types:new_instance_type"
    editor_overview_url_reverse_base = "instance_types:instance_type_overview"
    resource_type_name_singular = "instance type"
    resource_type_name_plural = "instance types"
    api_client_class = InstanceTypeApiClient
    column_metadata_api_client_class = InstanceTypeColumnMetadataApiClient


class InstanceTypeEditorStartFormView(InstanceTypeEditorView, EditorStartFormView):
    template_name = "instance_types/new_instance_type_start.html"
    form_class = InstanceTypeRegistrationForm
    success_url = reverse_lazy("instance_types:new_instance_type")


class InstanceTypeEditorProcessFormView(InstanceTypeEditorView, EditorProcessFormView):
    template_name = "instance_types/instance_type_editor.html"
    main_form_class = InstanceTypeEditorForm
    success_url = reverse_lazy("instance_types:new_instance_type")


class InstanceTypeListFormView(InstanceTypeEditorView, ResourceListFormView):
    new_resource_reverse = "instance_types:new_instance_type"


class InstanceTypeEditorOverviewTemplateView(
    InstanceTypeEditorView, EditorOverviewTemplateView
):
    pass
