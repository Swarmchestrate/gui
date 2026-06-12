import logging

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import FormView, TemplateView, View
from django.views.generic.base import ContextMixin

from .forms import (
    ColumnMetadataDeletionForm,
    MultiResourceDeletionForm,
    ResourceDeletionForm,
)

from editor.forms import FormWithDynamicallyPopulatedFields
from editor.view_helpers import get_form_config_for_table
from postgrest.table_names import TableNames
from utils.humanise import (
    humanise_resource_type,
    humanise_resource_type_plural,
)
from postgrest.api import ApiClient, Resource

logger = logging.getLogger(__name__)


# Create your views here.
class ResourceListContextMixin(ContextMixin):
    resource_list_reverse: str

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"resource_list_reverse": self.resource_list_reverse})
        return context


class ResourceListFormView(TemplateView):
    template_name = "resource_management/resource_list.html"
    resource_deletion_form_class = ResourceDeletionForm
    multi_resource_deletion_form_class = MultiResourceDeletionForm

    table_name: str
    resource_type: str

    resource_list_reverse: str
    new_resource_reverse: str
    resource_deletion_reverse: str
    multi_resource_deletion_reverse: str
    editor_reverse_base: str
    editor_overview_reverse_base: str
    tosca_template_download_reverse_base: str

    def get_resource_list(self):
        api_client = ApiClient()
        api_client.initialise_openapi_spec()
        return api_client.get_endpoint(self.table_name).get_resources()

    def dispatch(self, request, *args, **kwargs):
        self.resource_list = self.get_resource_list()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        context.update({
            "title": humanise_resource_type_plural(self.resource_type).title(),
            "new_resource_reverse": self.new_resource_reverse,
            "resource_deletion_reverse": self.resource_deletion_reverse,
            "resource_deletion_forms": {
                resource.pk: self.resource_deletion_form_class(
                    id_suffix=str(i),
                    initial={
                        "resource_id_to_delete": resource.pk
                    },
                )
                for i, resource in enumerate(self.resource_list)
            },
            "multi_resource_deletion_reverse": self.multi_resource_deletion_reverse,
            "multi_resource_deletion_form": self.multi_resource_deletion_form_class(
                resource_ids=[
                    resource.pk for resource in self.resource_list
                ]
            ),
            "resources": {
                resource.pk: resource
                for resource in self.resource_list
            },
            "editor_reverse_base": self.editor_reverse_base,
            "editor_overview_reverse_base": self.editor_overview_reverse_base,
            "tosca_template_download_reverse_base": self.tosca_template_download_reverse_base,
            "resource_type": self.resource_type,
        })
        return context


class ResourceDeletionFormView(FormView):
    form_class = ResourceDeletionForm

    table_name: str
    resource_type: str

    resource_list_reverse: str

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(self.resource_list_reverse)
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(
            self.request,
            f"The selected {humanise_resource_type(self.resource_type)} may not have been deleted as an error occurred during deletion. Please try again later.",
        )
        return redirect(self.resource_list_reverse)

    def form_valid(self, form):
        resource_id_to_delete = form.cleaned_data.get("resource_id_to_delete")
        api_client = ApiClient()
        api_client.initialise_openapi_spec()
        api_client.get_endpoint(self.table_name).delete(resource_id_to_delete)
        success_msg = f"Deleted {humanise_resource_type(self.resource_type)} {resource_id_to_delete}."
        messages.success(self.request, success_msg)
        return super().form_valid(form)


class MultiResourceDeletionFormView(FormView):
    form_class = MultiResourceDeletionForm

    api_client: ApiClient
    table_name: str
    resource_type: str

    resource_list_reverse: str

    def dispatch(self, request, *args, **kwargs):
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.resource_list = self.api_client.get_endpoint(self.table_name).get_resources()
        self.success_url = reverse_lazy(self.resource_list_reverse)
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "resource_ids": [
                resource.pk
                for resource in self.resource_list
            ]
        })
        return kwargs

    def form_invalid(self, form):
        messages.error(
            self.request,
            f"The selected {humanise_resource_type_plural(self.resource_type)} may not have been deleted as an error occurred during deletion. Please try again later.",
        )
        return redirect(self.resource_list_reverse)

    def form_valid(self, form):
        resource_ids_to_delete = [
            int(resource_id)
            for resource_id in form.cleaned_data.get("resource_ids_to_delete", [])
        ]
        self.api_client.get_endpoint(self.table_name).delete_many(resource_ids_to_delete)
        success_msg = f"Deleted 1 {humanise_resource_type(self.resource_type)}."
        if len(resource_ids_to_delete) != 1:
            success_msg = f"Deleted {len(resource_ids_to_delete)} {humanise_resource_type_plural(self.resource_type)}."
        messages.success(self.request, success_msg)
        return super().form_valid(form)


class ToscaTemplateDownloadView(View):
    resource_id: int
    table_name: str
    resource_type: str
    
    def generate_tosca_template(self) -> str:
        pass

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = kwargs["resource_id"]
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        tosca_template = self.generate_tosca_template()
        response = HttpResponse(
            tosca_template,
            content_type="application/yaml"
        )
        response["Content-Disposition"] = f"inline; filename={self.resource_type}_{self.resource_id}.yaml"
        return response


# Column metadata management
def _get_composite_pk(resource: Resource):
    return f"{resource.as_dict().get('table_name')}__{resource.as_dict().get('column_name')}"

class ColumnMetadataManagementView(TemplateView):
    template_name = "resource_management/column_metadata_list.html"
    resource_deletion_form_class = ResourceDeletionForm
    multi_resource_deletion_form_class = MultiResourceDeletionForm

    table_name = TableNames.COLUMN_METADATA
    resource_type = TableNames.COLUMN_METADATA

    resource_list_reverse = "resource_management:manage_column_metadata"
    new_resource_reverse = "resource_management:new_column_metadata"
    resource_update_reverse = "resource_management:update_column_metadata"
    resource_deletion_reverse = "resource_management:delete_column_metadata"
    multi_resource_deletion_reverse = "resource_management:delete_column_metadata_multi"

    def get_resource_list(self):
        api_client = ApiClient()
        api_client.initialise_openapi_spec()
        return api_client.get_endpoint(self.table_name).get_resources()

    def dispatch(self, request, *args, **kwargs):
        self.resource_list = self.get_resource_list()
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        self.column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        form_config = get_form_config_for_table(
            self.table_name,
            self.openapi_spec,
            self.column_metadata,
        )
        context.update({
            "title": humanise_resource_type_plural(self.resource_type).title(),
            "new_resource_reverse": self.new_resource_reverse,
            "new_resource_form": FormWithDynamicallyPopulatedFields(
                fields=form_config.get_fields(include_pk_fields=True)
            ),
            "resource_update_forms": {
                _get_composite_pk(resource): FormWithDynamicallyPopulatedFields(
                    fields=form_config.get_fields(),
                    initial=resource.as_dict()
                )
                for resource in self.resource_list
            },
            "resource_update_reverse": self.resource_update_reverse,
            "resource_deletion_reverse": self.resource_deletion_reverse,
            "resource_deletion_forms": {
                _get_composite_pk(resource): self.resource_deletion_form_class(
                    id_suffix=str(i),
                    initial={
                        "resource_id_to_delete": _get_composite_pk(resource)
                    },
                )
                for i, resource in enumerate(self.resource_list)
            },
            "multi_resource_deletion_reverse": self.multi_resource_deletion_reverse,
            "multi_resource_deletion_form": self.multi_resource_deletion_form_class(
                resource_ids=[
                    _get_composite_pk(resource)
                    for resource in self.resource_list
                ]
            ),
            "resources": {
                _get_composite_pk(resource): resource
                for resource in self.resource_list
            },
            "resource_type": self.resource_type,
        })
        return context


class NewColumnMetadataFormView(FormView):
    form_class = FormWithDynamicallyPopulatedFields
    success_url = reverse_lazy("resource_management:manage_column_metadata")
    table_name = TableNames.COLUMN_METADATA

    def dispatch(self, request, *args, **kwargs):
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        self.column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        table_name = form.cleaned_data["table_name"]
        column_name = form.cleaned_data["column_name"]
        self.api_client.get_endpoint(
            self.table_name
        ).register_with_composite_key(
            {
                "table_name": table_name,
                "column_name": column_name,
            },
            form.cleaned_data
        )
        messages.success(
            self.request,
            f"New {humanise_resource_type(self.resource_type)} registered.",
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        form_config = get_form_config_for_table(
            self.table_name,
            self.openapi_spec,
            self.column_metadata,
        )
        kwargs.update({
            "fields": form_config.get_fields(include_pk_fields=True)
        })
        return kwargs


class UpdateColumnMetadataFormView(FormView):
    form_class = FormWithDynamicallyPopulatedFields
    success_url = reverse_lazy("resource_management:manage_column_metadata")
    table_name = TableNames.COLUMN_METADATA

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = kwargs["resource_id"]
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.openapi_spec = self.api_client.openapi_spec
        self.column_metadata = self.api_client.get_endpoint("column_metadata").get_resources()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        update_data = form.cleaned_data
        try:
            table_name, column_name = self.resource_id.split("__")
            self.api_client.get_endpoint(self.table_name).update_by_composite_key(
                {
                    "table_name": table_name,
                    "column_name": column_name,
                },
                update_data
            )
        except Exception:
            error_msg = f"An error occurred whilst updating {humanise_resource_type(self.table_name)} {self.resource_id}. The update may not have been applied."
            logger.exception(error_msg)
            return self.form_invalid()

        message = f"Saved changes to {humanise_resource_type(self.table_name)} {self.resource_id}."
        messages.success(self.request, message)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        form_config = get_form_config_for_table(
            self.table_name,
            self.openapi_spec,
            self.column_metadata,
        )
        kwargs.update({
            "fields": form_config.get_fields()
        })
        return kwargs


class ColumnMetadataDeletionFormView(FormView):
    form_class = ColumnMetadataDeletionForm
    success_url = reverse_lazy("resource_management:manage_column_metadata")
    table_name = TableNames.COLUMN_METADATA
    resource_list_reverse = "resource_management:manage_column_metadata"

    resource_type: str

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(
            self.request,
            f"The selected {humanise_resource_type(self.resource_type)} may not have been deleted as an error occurred during deletion. Please try again later.",
        )
        return redirect(self.resource_list_reverse)

    def form_valid(self, form):
        resource_id_to_delete = form.cleaned_data.get("resource_id_to_delete")
        api_client = ApiClient()
        api_client.initialise_openapi_spec()
        table_name, column_name = resource_id_to_delete.split("__")
        api_client.get_endpoint(self.table_name).delete_by_composite_key({
            "table_name": table_name,
            "column_name": column_name,
        })
        success_msg = f"Deleted {humanise_resource_type(self.resource_type)}."
        messages.success(self.request, success_msg)
        return super().form_valid(form)


class MultiColumnMetadataDeletionFormView(FormView):
    success_url = reverse_lazy("resource_management:manage_column_metadata")
    form_class = MultiResourceDeletionForm
    table_name = TableNames.COLUMN_METADATA
    resource_list_reverse = "resource_management:manage_column_metadata"

    api_client: ApiClient
    resource_type: str

    def dispatch(self, request, *args, **kwargs):
        self.api_client = ApiClient()
        self.api_client.initialise_openapi_spec()
        self.resource_list = self.api_client.get_endpoint(self.table_name).get_resources()
        if not hasattr(self, "resource_type"):
            self.resource_type = self.table_name
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "resource_ids": [
                _get_composite_pk(resource)
                for resource in self.resource_list
            ]
        })
        return kwargs

    def form_invalid(self, form):
        messages.error(
            self.request,
            f"The selected {humanise_resource_type_plural(self.resource_type)} may not have been deleted as an error occurred during deletion. Please try again later.",
        )
        return redirect(self.resource_list_reverse)

    def form_valid(self, form):
        delete_conditions = list()
        for resource_id in form.cleaned_data.get("resource_ids_to_delete", []):
            table_name, column_name = resource_id.split("__")
            delete_conditions.append({
                "table_name": table_name,
                "column_name": column_name,
            })
        self.api_client.get_endpoint(self.table_name).delete_many_by_composite_key(
            delete_conditions
        )
        success_msg = f"Deleted 1 {humanise_resource_type(self.resource_type)}."
        if len(delete_conditions) != 1:
            success_msg = f"Deleted {len(delete_conditions)} {humanise_resource_type_plural(self.resource_type)}."
        messages.success(self.request, success_msg)
        return super().form_valid(form)
