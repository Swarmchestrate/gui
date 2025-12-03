import os

from django.conf import settings

from application_volumes.api.api_clients import (
    BaseApplicationVolumeApiClient,
)
from application_volumes.api.mocks.mock_definitions import (
    ApplicationVolumeUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)

BASE_DIR = settings.BASE_DIR


class ApplicationVolumeApiClient(BaseApplicationVolumeApiClient, MockApiClient):
    endpoint_definition_class = ApplicationVolumeUserSpecifiableOpenApiDefinition

    path_to_data = os.path.join(
        BASE_DIR,
        "application_volumes",
        "api",
        "mocks",
        "jsons",
        "data",
        "application_volumes.json",
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "application_volumes", "temp")


class ApplicationVolumeColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [r for r in resources if r.get("table_name") == "application_volume"]
