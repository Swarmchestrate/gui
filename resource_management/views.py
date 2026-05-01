import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.base import ContextMixin

from .forms import (
    MultiResourceDeletionForm,
    ResourceDeletionForm,
)

from utils.humanise import (
    humanise_resource_type,
    humanise_resource_type_plural,
)
from postgrest.new_api import ApiClient

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
    pk_field_name: str
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
