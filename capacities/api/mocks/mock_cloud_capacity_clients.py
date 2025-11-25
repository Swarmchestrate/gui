import os

from django.conf import settings

from capacities.api.capacity_api_clients import BaseCapacityApiClient
from capacities.api.cloud_capacity_api_clients import (
    BaseCloudCapacityColumnMetadataApiClient,
)
from capacities.api.mocks.mock_definitions import (
    CapacityUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)

BASE_DIR = settings.BASE_DIR


# Cloud Capacities
class CloudCapacityApiClient(BaseCapacityApiClient, MockApiClient):
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition
    path_to_data = os.path.join(
        BASE_DIR,
        "capacities",
        "api",
        "mocks",
        "jsons",
        "data",
        "cloud_capacities.json",
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "capacities", "temp")


class CloudCapacityColumnMetadataApiClient(
    BaseCloudCapacityColumnMetadataApiClient, MockColumnMetadataApiClient
):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [
            r
            for r in resources
            if (
                r.get("table_name") == "capacity"
                and r.get("category") not in self.disabled_categories
            )
        ]
