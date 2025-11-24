from editor.api.base_api_clients import (
    ApiEndpoint,
    BaseApiEndpoint,
    ColumnMetadataApiEndpoint,
)

from .definitions import LocalityUserSpecifiableOpenApiDefinition


class BaseLocalityApiEndpoint(BaseApiEndpoint):
    endpoint = "locality"


class LocalityApiEndpoint(BaseLocalityApiEndpoint, ApiEndpoint):
    endpoint_definition_class = LocalityUserSpecifiableOpenApiDefinition


class LocalityColumnMetadataApiEndpoint(ColumnMetadataApiEndpoint):
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.locality",
            }
        )
        return super().get_registrations(params=params)
