from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)

from .definitions import CapacityOperatingSystemUserSpecifiableOpenApiDefinition


class BaseCapacityOperatingSystemApiClient(BaseApiClient):
    endpoint = "capacity_operating_system"


class CapacityOperatingSystemApiClient(BaseCapacityOperatingSystemApiClient, ApiClient):
    endpoint_definition_class = CapacityOperatingSystemUserSpecifiableOpenApiDefinition


class CapacityOperatingSystemColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.capacity_operating_system",
            }
        )
        return super().get_resources(params=params)
