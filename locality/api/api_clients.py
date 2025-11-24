from editor.api.base_api_clients import ApiEndpoint, ColumnMetadataApiEndpoint

from .definitions import LocalityUserSpecifiableOpenApiDefinition


class LocalityApiEndpoint(ApiEndpoint):
    endpoint_definition_class = LocalityUserSpecifiableOpenApiDefinition

    def __init__(self) -> None:
        self.endpoint = "locality"
        super().__init__()


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
