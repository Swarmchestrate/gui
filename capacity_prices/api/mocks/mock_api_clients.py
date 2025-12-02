import os

from django.conf import settings

from capacity_prices.api.api_clients import (
    BaseCapacityPriceApiClient,
)
from capacity_prices.api.mocks.mock_definitions import (
    CapacityPriceUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)

BASE_DIR = settings.BASE_DIR


class CapacityPriceApiClient(BaseCapacityPriceApiClient, MockApiClient):
    endpoint_definition_class = CapacityPriceUserSpecifiableOpenApiDefinition
    path_to_data = os.path.join(
        BASE_DIR,
        "capacity_prices",
        "api",
        "mocks",
        "jsons",
        "data",
        "capacity_prices.json",
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "capacity_prices", "temp")


class CapacityPriceColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [r for r in resources if r.get("table_name") == "capacity_price"]
