from django import forms
from django.contrib import messages
from django.urls.base import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.base import ContextMixin

from editor.api.base_api_clients import ApiClient, ColumnMetadataApiClient

from .forms import OpenApiSpecificationBasedFormWithSuffix, ResourceDeletionForm


# Create your views here.
class ResourceListContextMixin(ContextMixin):
    editor_resource_list_url_reverse: str

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "editor_resource_list_url_reverse": self.editor_resource_list_url_reverse,
            }
        )
        return context


class NewResourceFormView(FormView):
    form_class: type[forms.Form]

    api_client: ApiClient
    column_metadata_api_client: ColumnMetadataApiClient
    id_field: str
    resource_type_name_singular: str

    editor_resource_list_url_reverse: str

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy(self.editor_resource_list_url_reverse)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "api_client": self.api_client,
                "column_metadata_api_client": self.column_metadata_api_client,
            }
        )
        return kwargs

    def form_invalid(self, form):
        messages.error(
            self.request,
            "The form submitted was not valid.",
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        new_resource = self.api_client.register(form.cleaned_data)
        success_msg = f"Registered {self.resource_type_name_singular} {new_resource.get(self.id_field)}."
        messages.success(self.request, success_msg)
        return super().form_valid(form)


class ResourceUpdateFormView(FormView):
    form_class: type[forms.Form]

    api_client: ApiClient
    column_metadata_api_client: ColumnMetadataApiClient
    id_field: str
    resource_type_name_singular: str

    editor_resource_list_url_reverse: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs["resource_id"]
        self.success_url = reverse_lazy(self.editor_resource_list_url_reverse)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "api_client": self.api_client,
                "column_metadata_api_client": self.column_metadata_api_client,
            }
        )
        return kwargs

    def form_invalid(self, form):
        messages.error(
            self.request,
            "The form submitted was not valid.",
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        self.api_client.update(self.resource_id, form.cleaned_data)
        success_msg = f"Updated {self.resource_type_name_singular}."
        messages.success(self.request, success_msg)
        return super().form_valid(form)


class ResourceDeletionFormView(FormView):
    form_class = ResourceDeletionForm

    api_client: ApiClient
    id_field: str
    resource_type_name_singular: str
    resource_type_name_plural: str

    editor_resource_list_url_reverse: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_list = self.api_client.get_resources()
        self.success_url = reverse_lazy(self.editor_resource_list_url_reverse)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "resource_ids": [
                    resource.get(self.id_field) for resource in self.resource_list
                ]
            }
        )
        return kwargs

    def form_invalid(self, form):
        messages.error(
            self.request,
            f"The selected {self.resource_type_name_plural} may not have been deleted as an error occurred during deletion. Please try again later.",
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        resource_ids_to_delete = [
            int(resource_id)
            for resource_id in form.cleaned_data.get("resource_ids_to_delete", [])
        ]
        self.api_client.delete_many(resource_ids_to_delete)
        success_msg = f"Deleted 1 {self.resource_type_name_singular}."
        if len(resource_ids_to_delete) != 1:
            success_msg = f"Deleted {len(resource_ids_to_delete)} {self.resource_type_name_plural}."
        messages.success(self.request, success_msg)
        return super().form_valid(form)


class ResourceListFormView(TemplateView):
    template_name = "resource_management/resource_list.html"
    resource_deletion_form_class: type[ResourceDeletionForm] = ResourceDeletionForm

    api_client: ApiClient
    column_metadata_api_client: ColumnMetadataApiClient
    id_field: str
    resource_type_name_plural: str

    editor_resource_list_url_reverse: str
    new_resource_reverse: str
    resource_deletion_reverse: str

    def dispatch(self, request, *args, **kwargs):
        self.resource_list = self.api_client.get_resources()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": self.resource_type_name_plural.title(),
                "new_resource_reverse": self.new_resource_reverse,
                "resource_deletion_reverse": self.resource_deletion_reverse,
                "delete_form": self.resource_deletion_form_class(
                    resource_ids=[
                        resource[self.id_field] for resource in self.resource_list
                    ]
                ),
                "resources": {
                    resource.get(self.id_field): resource
                    for resource in self.resource_list
                },
            }
        )
        return context


class BasicResourceListFormView(ResourceListFormView):
    new_resource_form_class: type[forms.Form]
    resource_update_form_class: type[OpenApiSpecificationBasedFormWithSuffix]

    resource_update_reverse: str

    def get_context_data(self, **kwargs):
        resource_update_forms = {
            resource.get(self.id_field): self.resource_update_form_class(
                self.api_client,
                self.column_metadata_api_client,
                id_suffix=str(i),
                initial=resource,
            )
            for i, resource in enumerate(self.resource_list)
        }
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "new_resource_reverse": self.new_resource_reverse,
                "resource_update_reverse": self.resource_update_reverse,
                "new_resource_form": self.new_resource_form_class(
                    self.api_client, self.column_metadata_api_client
                ),
                "resource_update_forms": resource_update_forms,
            }
        )
        return context
