from application_environment_vars.api.definitions import (
    ApplicationEnvironmentVarsUserSpecifiableOpenApiDefinition,
)
from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)


class BaseApplicationEnvironmentVarsApiClient(BaseApiClient):
    endpoint = "application_environment_var"


class ApplicationEnvironmentVarsApiClient(
    BaseApplicationEnvironmentVarsApiClient, ApiClient
):
    endpoint_definition_class = (
        ApplicationEnvironmentVarsUserSpecifiableOpenApiDefinition
    )


class ApplicationEnvironmentVarsColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.application_environment_var",
            }
        )
        return super().get_resources(params=params)
