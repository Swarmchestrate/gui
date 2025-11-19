import os

from django.conf import settings

from editor.mocks.api_endpoint_client import (
    MockApiEndpointClient,
    MockColumnMetadataApiEndpointClient,
)

from .definitions import CapacityUserSpecifiableOpenApiDefinition

BASE_DIR = settings.BASE_DIR


# Cloud Capacities
class CloudCapacityApiEndpointClient(MockApiEndpointClient):
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition
    path_to_data = os.path.join(
        BASE_DIR, "capacities", "mocks", "data", "cloud_capacities.json"
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "capacities", "temp")


class CloudCapacityColumnMetadataApiEndpointClient(MockColumnMetadataApiEndpointClient):
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
class EdgeCapacityApiEndpointClient(MockApiEndpointClient):
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition
    path_to_data = os.path.join(
        BASE_DIR, "capacities", "mocks", "data", "edge_capacities.json"
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "capacities", "temp")


class EdgeCapacityColumnMetadataApiEndpointClient(MockColumnMetadataApiEndpointClient):
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
