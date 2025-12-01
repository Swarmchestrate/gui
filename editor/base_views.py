import logging

from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from .api.base_api_clients import ApiClient, ColumnMetadataApiClient

logger = logging.getLogger(__name__)


class ApiClientTemplateView(TemplateView):
    api_client_class: type[ApiClient]

    def setup(self, request, *args, **kwargs):
        self.api_client = self.api_client_class()
        self.id_field = self.api_client.endpoint_definition.id_field
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "id_field": self.id_field,
                "description": self.api_client.endpoint_definition.description,
            }
        )
        return context


class EditorContextMixin(ContextMixin):
    editor_start_reverse_base: str
    editor_reverse_base: str
    editor_overview_reverse_base: str

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "editor_reverse_base": self.editor_reverse_base,
                "editor_start_reverse_base": self.editor_start_reverse_base,
                "editor_overview_reverse_base": self.editor_overview_reverse_base,
            }
        )
        return context


class ColumnMetadataApiClientTemplateView(TemplateView):
    column_metadata_api_client_class: type[ColumnMetadataApiClient]

    def setup(self, request, *args, **kwargs):
        self.column_metadata_api_client = self.column_metadata_api_client_class()
        return super().setup(request, *args, **kwargs)


class ResourceTypeNameContextMixin(ContextMixin):
    resource_type_readable: str
    resource_type_readable_plural: str

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "resource_type_readable": self.resource_type_readable,
                "resource_type_readable_plural": self.resource_type_readable_plural,
            }
        )
        return context
