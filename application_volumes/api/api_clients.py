from application_volumes.api.definitions import (
    ApplicationVolumeUserSpecifiableOpenApiDefinition,
)
from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)


class BaseApplicationVolumeApiClient(BaseApiClient):
    endpoint = "application_volume"


class ApplicationVolumeApiClient(BaseApplicationVolumeApiClient, ApiClient):
    endpoint_definition_class = ApplicationVolumeUserSpecifiableOpenApiDefinition


class ApplicationVolumeColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.application_volume",
            }
        )
        return super().get_resources(params=params)
