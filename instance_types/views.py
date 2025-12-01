from django.urls import reverse_lazy

from editor.base_views import (
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    EditorContextMixin,
    ResourceTypeNameContextMixin,
)
from editor.views import (
    EditorOverviewTemplateView,
    EditorProcessFormView,
    EditorStartFormView,
)
from resource_management.views import (
    BasicResourceListFormView,
    MultiResourceDeletionFormView,
    NewResourceFormView,
    ResourceDeletionFormView,
    ResourceListContextMixin,
    ResourceUpdateFormView,
)

# from .api.api_clients import (
#     InstanceTypeApiClient,
#     InstanceTypeColumnMetadataApiClient,
# )
from .api.mocks.mock_api_clients import (
    InstanceTypeApiClient,
    InstanceTypeColumnMetadataApiClient,
)
from .forms import (
    InstanceTypeEditorForm,
    InstanceTypeRegistrationForm,
    InstanceTypeUpdateForm,
)
from .utils import instance_type_type_readable, instance_type_type_readable_plural


class InstanceTypeViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientTemplateView,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = InstanceTypeApiClient
    column_metadata_api_client_class = InstanceTypeColumnMetadataApiClient
    resource_list_reverse = "instance_types:instance_type_list"
    resource_update_reverse = "instance_types:update_instance_type"
    new_resource_reverse = "instance_types:new_instance_type"
    resource_deletion_reverse = "instance_types:delete_instance_type"
    multi_resource_deletion_reverse = "instance_types:delete_instance_types"
    resource_type_readable = instance_type_type_readable()
    resource_type_readable_plural = instance_type_type_readable_plural()


class InstanceTypeListFormView(InstanceTypeViewMixin, BasicResourceListFormView):
    template_name = "instance_types/instance_types.html"
    new_resource_form_class = InstanceTypeRegistrationForm
    resource_update_form_class = InstanceTypeUpdateForm


class NewInstanceTypeFormView(InstanceTypeViewMixin, NewResourceFormView):
    template_name = "instance_types/instance_types.html"
    new_resource_form_class = InstanceTypeRegistrationForm
    resource_update_form_class = InstanceTypeUpdateForm
    form_class = InstanceTypeRegistrationForm


class InstanceTypeUpdateFormView(InstanceTypeViewMixin, ResourceUpdateFormView):
    template_name = "instance_types/instance_types.html"
    new_resource_form_class = InstanceTypeRegistrationForm
    resource_update_form_class = InstanceTypeUpdateForm
    form_class = InstanceTypeUpdateForm


class InstanceTypeDeletionFormView(InstanceTypeViewMixin, ResourceDeletionFormView):
    pass


class MultiInstanceTypeDeletionFormView(
    InstanceTypeViewMixin, MultiResourceDeletionFormView
):
    pass


class InstanceTypeEditorStartFormView(InstanceTypeViewMixin, EditorStartFormView):
    template_name = "instance_types/new_instance_type_start.html"
    form_class = InstanceTypeRegistrationForm
    success_url = reverse_lazy("instance_types:new_instance_type")


class InstanceTypeEditorProcessFormView(InstanceTypeViewMixin, EditorProcessFormView):
    template_name = "instance_types/instance_type_editor.html"
    main_form_class = InstanceTypeEditorForm
    success_url = reverse_lazy("instance_types:new_instance_type")


class InstanceTypeEditorOverviewTemplateView(
    InstanceTypeViewMixin, EditorOverviewTemplateView
):
    pass
