import os

from django.conf import settings

from capacities.api.endpoints.abc import BaseEdgeCapacityColumnMetadataApiEndpoint
from capacities.mocks.definitions import CapacityUserSpecifiableOpenApiDefinition
from editor.mocks.endpoints.base import (
    MockApiEndpoint,
    MockColumnMetadataApiEndpoint,
)

BASE_DIR = settings.BASE_DIR


# Edge Capacities
class EdgeCapacityApiEndpoint(MockApiEndpoint):
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition
    path_to_data = os.path.join(
        BASE_DIR, "capacities", "mocks", "jsons", "data", "edge_capacities.json"
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "capacities", "temp")


class EdgeCapacityColumnMetadataApiEndpoint(
    BaseEdgeCapacityColumnMetadataApiEndpoint, MockColumnMetadataApiEndpoint
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
