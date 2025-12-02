from application_environment_vars.api.definitions import (
    ApplicationEnvironmentVarUserSpecifiableOpenApiDefinition,
)
from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)


class BaseApplicationEnvironmentVarApiClient(BaseApiClient):
    endpoint = "application_environment_var"


class ApplicationEnvironmentVarApiClient(
    BaseApplicationEnvironmentVarApiClient, ApiClient
):
    endpoint_definition_class = (
        ApplicationEnvironmentVarUserSpecifiableOpenApiDefinition
    )


class ApplicationEnvironmentVarColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.application_environment_var",
            }
        )
        return super().get_resources(params=params)
