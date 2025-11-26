import logging

from django.views.generic.base import ContextMixin

from .api.base_api_clients import ApiClient, ColumnMetadataApiClient

logger = logging.getLogger(__name__)


class ApiClientContextMixin(ContextMixin):
    api_client_class: type[ApiClient]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_client = self.api_client_class()
        self.id_field = self.api_client.endpoint_definition.id_field

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
    editor_start_url_reverse_base: str
    editor_url_reverse_base: str
    editor_overview_url_reverse_base: str

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "editor_url_reverse_base": self.editor_url_reverse_base,
                "editor_start_url_reverse_base": self.editor_start_url_reverse_base,
                "editor_overview_url_reverse_base": self.editor_overview_url_reverse_base,
            }
        )
        return context


class ColumnMetadataApiClientMixin:
    column_metadata_api_client_class: type[ColumnMetadataApiClient]


class ResourceTypeNameContextMixin(ContextMixin):
    resource_type_name_singular: str
    resource_type_name_plural: str

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "resource_type_name_singular": self.resource_type_name_singular,
                "resource_type_name_plural": self.resource_type_name_plural,
            }
        )
        return context
