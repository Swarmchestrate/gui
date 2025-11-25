import os

from django.conf import settings

from capacities.api.capacity_api_clients import BaseCapacityApiClient
from capacities.api.edge_capacity_api_clients import (
    BaseEdgeCapacityColumnMetadataApiClient,
)
from capacities.api.mocks.mock_definitions import (
    CapacityUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)

BASE_DIR = settings.BASE_DIR


# Edge Capacities
class EdgeCapacityApiClient(BaseCapacityApiClient, MockApiClient):
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition
    path_to_data = os.path.join(
        BASE_DIR,
        "capacities",
        "api",
        "mocks",
        "jsons",
        "data",
        "edge_capacities.json",
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "capacities", "temp")


class EdgeCapacityColumnMetadataApiClient(
    BaseEdgeCapacityColumnMetadataApiClient, MockColumnMetadataApiClient
):
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        registrations = super().get_registrations()
        return [
            r
            for r in registrations
            if (
                r.get("table_name") == "capacity"
                and r.get("category") not in self.disabled_categories
            )
        ]
