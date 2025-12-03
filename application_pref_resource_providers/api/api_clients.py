from application_pref_resource_providers.api.definitions import (
    ApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition,
)
from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)


class BaseApplicationPrefResourceProviderApiClient(BaseApiClient):
    endpoint = "application_pref_resource_provider"


class ApplicationPrefResourceProviderApiClient(
    BaseApplicationPrefResourceProviderApiClient, ApiClient
):
    endpoint_definition_class = (
        ApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition
    )


class ApplicationPrefResourceProviderColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.application_pref_resource_provider",
            }
        )
        return super().get_resources(params=params)
