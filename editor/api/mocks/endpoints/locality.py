import os

from django.conf import settings

from editor.api.mocks.definitions.user_specifiable_definitions import (
    LocalityUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.endpoints.base import (
    MockApiEndpoint,
    MockColumnMetadataApiEndpoint,
)

BASE_DIR = settings.BASE_DIR


# Cloud Capacities
class LocalityApiEndpoint(MockApiEndpoint):
    endpoint = "locality"
    endpoint_definition_class = LocalityUserSpecifiableOpenApiDefinition
    path_to_data = os.path.join(
        BASE_DIR,
        "editor",
        "api",
        "mocks",
        "jsons",
        "data",
        "localities.json",
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "editor", "temp")


class LocalityColumnMetadataApiEndpoint(MockColumnMetadataApiEndpoint):
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        registrations = super().get_registrations()
        return [r for r in registrations if r.get("table_name") == "capacity"]
