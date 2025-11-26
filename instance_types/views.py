from django.urls import reverse_lazy

from editor.base_views import (
    ApiClientTemplateView,
    ColumnMetadataApiClientMixin,
    EditorContextMixin,
    ResourceTypeNameContextMixin,
)
from editor.views import (
    EditorOverviewTemplateView,
    EditorProcessFormView,
    EditorStartFormView,
)
from resource_management.views import ResourceListContextMixin, ResourceListFormView

# from .api.api_clients import (
#     InstanceTypeApiClient,
#     InstanceTypeColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    InstanceTypeApiClient,
    InstanceTypeColumnMetadataApiClient,
)
from .forms import InstanceTypeEditorForm, InstanceTypeRegistrationForm


class InstanceTypeViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientMixin,
    EditorContextMixin,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = InstanceTypeApiClient
    editor_url_reverse_base = "instance_types:instance_type_editor"
    editor_start_url_reverse_base = "instance_types:new_instance_type"
    editor_overview_url_reverse_base = "instance_types:instance_type_overview"
    column_metadata_api_client_class = InstanceTypeColumnMetadataApiClient
    editor_resource_list_url_reverse = "instance_types:instance_type_list"
    resource_type_name_singular = "instance type"
    resource_type_name_plural = "instance types"


class InstanceTypeEditorStartFormView(InstanceTypeViewMixin, EditorStartFormView):
    template_name = "instance_types/new_instance_type_start.html"
    form_class = InstanceTypeRegistrationForm
    success_url = reverse_lazy("instance_types:new_instance_type")


class InstanceTypeEditorProcessFormView(InstanceTypeViewMixin, EditorProcessFormView):
    template_name = "instance_types/instance_type_editor.html"
    main_form_class = InstanceTypeEditorForm
    success_url = reverse_lazy("instance_types:new_instance_type")


class InstanceTypeListFormView(InstanceTypeViewMixin, ResourceListFormView):
    new_resource_reverse = "instance_types:new_instance_type"


class InstanceTypeEditorOverviewTemplateView(
    InstanceTypeViewMixin, EditorOverviewTemplateView
):
    pass
