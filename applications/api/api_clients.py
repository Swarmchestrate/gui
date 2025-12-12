from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)

from .definitions import (
    ApplicationMicroserviceUserSpecifiableOpenApiDefinition,
    ApplicationUserSpecifiableOpenApiDefinition,
)


class BaseApplicationApiClient(BaseApiClient):
    endpoint = "application"


class ApplicationApiClient(BaseApplicationApiClient, ApiClient):
    endpoint_definition_class = ApplicationUserSpecifiableOpenApiDefinition


class BaseApplicationMicroserviceApiClient(BaseApiClient):
    endpoint = "application_microservice"


class ApplicationMicroserviceApiClient(BaseApplicationApiClient, ApiClient):
    endpoint_definition_class = ApplicationMicroserviceUserSpecifiableOpenApiDefinition


class ApplicationColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.application",
            }
        )
        return super().get_resources(params=params)


class ApplicationMicroserviceColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.application_microservice",
            }
        )
        return super().get_resources(params=params)
