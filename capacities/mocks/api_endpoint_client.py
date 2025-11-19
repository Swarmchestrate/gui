import os

from django.conf import settings

from editor.mocks.api_endpoint_client import (
    MockApiEndpoint,
    MockColumnMetadataApiEndpoint,
)

from .definitions import CapacityUserSpecifiableOpenApiDefinition

BASE_DIR = settings.BASE_DIR


# Cloud Capacities
class CloudCapacityApiEndpoint(MockApiEndpoint):
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition
    path_to_data = os.path.join(
        BASE_DIR, "capacities", "mocks", "data", "cloud_capacities.json"
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "capacities", "temp")


class CloudCapacityColumnMetadataApiEndpoint(MockColumnMetadataApiEndpoint):
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        registrations = super().get_registrations()
        return [
            r
            for r in registrations
            if (
                r.get("table_name") == "capacity"
                and r.get("category") != "Edge Specific"
            )
        ]


# Edge Capacities
class EdgeCapacityApiEndpoint(MockApiEndpoint):
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition
    path_to_data = os.path.join(
        BASE_DIR, "capacities", "mocks", "data", "edge_capacities.json"
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "capacities", "temp")


class EdgeCapacityColumnMetadataApiEndpoint(MockColumnMetadataApiEndpoint):
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        registrations = super().get_registrations()
        return [
            r
            for r in registrations
            if (
                r.get("table_name") == "capacity"
                and r.get("category") != "System Specific"
            )
        ]
