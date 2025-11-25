from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)

from .definitions import LocalityUserSpecifiableOpenApiDefinition


class BaseLocalityApiClient(BaseApiClient):
    endpoint = "locality"


class LocalityApiClient(BaseLocalityApiClient, ApiClient):
    endpoint_definition_class = LocalityUserSpecifiableOpenApiDefinition


class LocalityColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.locality",
            }
        )
        return super().get_registrations(params=params)
