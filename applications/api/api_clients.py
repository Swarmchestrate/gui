from editor.api.base_api_clients import (
    ApiEndpoint,
    BaseApiEndpoint,
    ColumnMetadataApiEndpoint,
)

from .definitions import ApplicationUserSpecifiableOpenApiDefinition


class BaseApplicationApiEndpoint(BaseApiEndpoint):
    endpoint = "application"


class ApplicationApiEndpoint(BaseApplicationApiEndpoint, ApiEndpoint):
    endpoint_definition_class = ApplicationUserSpecifiableOpenApiDefinition


class ApplicationColumnMetadataApiEndpoint(ColumnMetadataApiEndpoint):
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.application",
            }
        )
        return super().get_registrations(params=params)
