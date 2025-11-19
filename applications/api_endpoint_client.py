from editor.api_endpoint_client import (
    ApiEndpoint,
    ColumnMetadataApiEndpoint,
)

from .definitions import ApplicationUserSpecifiableOpenApiDefinition


class ApplicationApiEndpoint(ApiEndpoint):
    endpoint_definition_class = ApplicationUserSpecifiableOpenApiDefinition

    def __init__(self) -> None:
        self.endpoint = "application"
        super().__init__()


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
