from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)

from .definitions import ApplicationUserSpecifiableOpenApiDefinition


class BaseApplicationApiClient(BaseApiClient):
    endpoint = "application"


class ApplicationApiClient(BaseApplicationApiClient, ApiClient):
    endpoint_definition_class = ApplicationUserSpecifiableOpenApiDefinition


class ApplicationColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.application",
            }
        )
        return super().get_registrations(params=params)
