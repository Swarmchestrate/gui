from django.contrib import messages
from django.views.generic import FormView, TemplateView

from editor.base_views import (
    ApiClientTemplateView,
    EditorTemplateView,
    ResourceTypeNameTemplateView,
)

from .forms import ResourceDeletionForm


# Create your views here.
class ResourceListViewMixin:
    editor_resource_list_url_reverse: str


class ResourceListTemplateView(ResourceListViewMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "editor_resource_list_url_reverse": self.editor_resource_list_url_reverse,
            }
        )
        return context


class ResourceListFormView(
    ApiClientTemplateView, EditorTemplateView, ResourceTypeNameTemplateView, FormView
):
    template_name = "resource_management/resource_list.html"
    form_class = ResourceDeletionForm

    new_resource_reverse: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource_list = self.api_client.get_resources()

    def dispatch(self, request, *args, **kwargs):
        self.success_url = request.path
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": self.resource_type_name_plural.title(),
                "resources": {
                    resource.get(self.id_field): resource
                    for resource in self.resource_list
                },
                "new_resource_reverse": self.new_resource_reverse,
            }
        )
        return context

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
        resource_ids_to_delete = form.cleaned_data.get("resource_ids_to_delete", [])
        self.api_client.delete_many(resource_ids_to_delete)
        success_msg = f"Deleted 1 {self.resource_type_name_singular}"
        if len(resource_ids_to_delete) != 1:
            success_msg = f"Deleted {len(resource_ids_to_delete)} {self.resource_type_name_plural}"
        messages.success(self.request, success_msg)
        return super().form_valid(form)
