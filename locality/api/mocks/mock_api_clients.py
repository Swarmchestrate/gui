import os

from django.conf import settings

from editor.api.mocks.mock_base_api_clients import (
    MockApiEndpoint,
    MockColumnMetadataApiEndpoint,
)
from locality.api.api_clients import BaseLocalityApiEndpoint
from locality.api.mocks.mock_definitions import (
    LocalityUserSpecifiableOpenApiDefinition,
)

BASE_DIR = settings.BASE_DIR


# Cloud Capacities
class LocalityApiEndpoint(BaseLocalityApiEndpoint, MockApiEndpoint):
    endpoint_definition_class = LocalityUserSpecifiableOpenApiDefinition
    path_to_data = os.path.join(
        BASE_DIR,
        "locality",
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
