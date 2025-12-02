from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)

from .definitions import CapacityPriceUserSpecifiableOpenApiDefinition


class BaseCapacityPriceApiClient(BaseApiClient):
    endpoint = "capacity_price"


class CapacityPriceApiClient(BaseCapacityPriceApiClient, ApiClient):
    endpoint_definition_class = CapacityPriceUserSpecifiableOpenApiDefinition


class CapacityPriceColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.capacity_price",
            }
        )
        return super().get_resources(params=params)
