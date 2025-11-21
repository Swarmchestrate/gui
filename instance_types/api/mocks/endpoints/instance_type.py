import os

from django.conf import settings

from editor.api.mocks.endpoints.base import (
    MockApiEndpoint,
    MockColumnMetadataApiEndpoint,
)
from instance_types.api.mocks.definitions.user_specifiable_definitions import (
    CapacityInstanceTypeUserSpecifiableOpenApiDefinition,
)

BASE_DIR = settings.BASE_DIR


class InstanceTypeApiEndpoint(MockApiEndpoint):
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

    def _prepare_update_data(self, data: dict):
        data = super()._prepare_update_data(data)
        data.pop("updated_at", None)
        data.pop(self.endpoint_definition.id_field, None)
        return data


class InstanceTypeColumnMetadataApiEndpoint(MockColumnMetadataApiEndpoint):
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        registrations = super().get_registrations()
        return [
            r for r in registrations if r.get("table_name") == "capacity_instance_type"
        ]
