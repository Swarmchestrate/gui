import os

from django.conf import settings

from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)
from instance_types.api.api_clients import BaseInstanceTypeApiClient
from instance_types.api.mocks.mock_definitions import (
    CapacityInstanceTypeUserSpecifiableOpenApiDefinition,
)

BASE_DIR = settings.BASE_DIR


class InstanceTypeApiClient(BaseInstanceTypeApiClient, MockApiClient):
    endpoint_definition_class = CapacityInstanceTypeUserSpecifiableOpenApiDefinition

    path_to_data = os.path.join(
        BASE_DIR,
        "instance_types",
        "api",
        "mocks",
        "jsons",
        "data",
        "instance_types.json",
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "instance_types", "temp")


class InstanceTypeColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [r for r in resources if r.get("table_name") == "capacity_instance_type"]
