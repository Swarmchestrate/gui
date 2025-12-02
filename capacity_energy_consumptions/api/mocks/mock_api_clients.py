import os

from django.conf import settings

from capacity_energy_consumptions.api.api_clients import (
    BaseCapacityEnergyConsumptionApiClient,
)
from capacity_energy_consumptions.api.mocks.mock_definitions import (
    CapacityEnergyConsumptionUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)

BASE_DIR = settings.BASE_DIR


class CapacityEnergyConsumptionApiClient(
    BaseCapacityEnergyConsumptionApiClient, MockApiClient
):
    endpoint_definition_class = (
        CapacityEnergyConsumptionUserSpecifiableOpenApiDefinition
    )
    path_to_data = os.path.join(
        BASE_DIR,
        "capacity_energy_consumptions",
        "api",
        "mocks",
        "jsons",
        "data",
        "capacity_energy_consumptions.json",
    )
    path_to_temp_data_dir = os.path.join(
        BASE_DIR, "capacity_energy_consumptions", "temp"
    )


class CapacityEnergyConsumptionColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [
            r for r in resources if r.get("table_name") == "capacity_energy_consumption"
        ]
