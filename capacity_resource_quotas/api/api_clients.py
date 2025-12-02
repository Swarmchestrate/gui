from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)

from .definitions import CapacityResourceQuotaUserSpecifiableOpenApiDefinition


class BaseCapacityResourceQuotaApiClient(BaseApiClient):
    endpoint = "capacity_resource_quota"


class CapacityResourceQuotaApiClient(BaseCapacityResourceQuotaApiClient, ApiClient):
    endpoint_definition_class = CapacityResourceQuotaUserSpecifiableOpenApiDefinition


class CapacityResourceQuotaColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.capacity_resource_quota",
            }
        )
        return super().get_resources(params=params)
