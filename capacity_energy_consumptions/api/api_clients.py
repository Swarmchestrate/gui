from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)

from .definitions import CapacityEnergyConsumptionUserSpecifiableOpenApiDefinition


class BaseCapacityEnergyConsumptionApiClient(BaseApiClient):
    endpoint = "capacity_energy_consumption"


class CapacityEnergyConsumptionApiClient(
    BaseCapacityEnergyConsumptionApiClient, ApiClient
):
    endpoint_definition_class = (
        CapacityEnergyConsumptionUserSpecifiableOpenApiDefinition
    )


class CapacityEnergyConsumptionColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.capacity_energy_consumption",
            }
        )
        return super().get_resources(params=params)
