import os

from django.conf import settings

from capacity_operating_systems.api.api_clients import (
    BaseCapacityOperatingSystemApiClient,
)
from capacity_operating_systems.api.mocks.mock_definitions import (
    CapacityOperatingSystemUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)

BASE_DIR = settings.BASE_DIR


class CapacityOperatingSystemApiClient(
    BaseCapacityOperatingSystemApiClient, MockApiClient
):
    endpoint_definition_class = CapacityOperatingSystemUserSpecifiableOpenApiDefinition
    path_to_data = os.path.join(
        BASE_DIR,
        "capacity_operating_systems",
        "api",
        "mocks",
        "jsons",
        "data",
        "capacity_operating_systems.json",
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "capacity_operating_systems", "temp")


class CapacityOperatingSystemColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [
            r for r in resources if r.get("table_name") == "capacity_operating_system"
        ]
