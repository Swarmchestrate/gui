import os

from django.conf import settings

from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)
from locality.api.api_clients import BaseLocalityApiClient
from locality.api.mocks.mock_definitions import (
    LocalityUserSpecifiableOpenApiDefinition,
)

BASE_DIR = settings.BASE_DIR


# Cloud Capacities
class LocalityApiClient(BaseLocalityApiClient, MockApiClient):
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


class LocalityColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [r for r in resources if r.get("table_name") == "capacity"]
