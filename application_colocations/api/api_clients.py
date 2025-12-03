from application_colocations.api.definitions import (
    ApplicationColocateUserSpecifiableOpenApiDefinition,
)
from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)


class BaseApplicationColocateApiClient(BaseApiClient):
    endpoint = "application_colocate"


class ApplicationColocateApiClient(BaseApplicationColocateApiClient, ApiClient):
    endpoint_definition_class = ApplicationColocateUserSpecifiableOpenApiDefinition


class ApplicationColocateColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.application_colocate",
            }
        )
        return super().get_resources(params=params)
