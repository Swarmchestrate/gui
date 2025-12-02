import os

from django.conf import settings

from capacity_instance_types.api.api_clients import BaseCapacityInstanceTypeApiClient
from capacity_instance_types.api.mocks.mock_definitions import (
    CapacityInstanceTypeUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)

BASE_DIR = settings.BASE_DIR


class CapacityInstanceTypeApiClient(BaseCapacityInstanceTypeApiClient, MockApiClient):
    endpoint_definition_class = CapacityInstanceTypeUserSpecifiableOpenApiDefinition

    path_to_data = os.path.join(
        BASE_DIR,
        "capacity_instance_types",
        "api",
        "mocks",
        "jsons",
        "data",
        "capacity_instance_types.json",
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "capacity_instance_types", "temp")


class CapacityInstanceTypeColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [r for r in resources if r.get("table_name") == "capacity_instance_type"]
