import os

from django.conf import settings

from editor.api.mocks.mock_base_api_clients import (
    MockApiEndpoint,
    MockColumnMetadataApiEndpoint,
)
from instance_types.api.api_clients import BaseInstanceTypeApiEndpoint
from instance_types.api.mocks.mock_definitions import (
    CapacityInstanceTypeUserSpecifiableOpenApiDefinition,
)

BASE_DIR = settings.BASE_DIR


class InstanceTypeApiEndpoint(BaseInstanceTypeApiEndpoint, MockApiEndpoint):
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


class InstanceTypeColumnMetadataApiEndpoint(MockColumnMetadataApiEndpoint):
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        registrations = super().get_registrations()
        return [
            r for r in registrations if r.get("table_name") == "capacity_instance_type"
        ]
