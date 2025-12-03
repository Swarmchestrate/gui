import os

from django.conf import settings

from application_colocations.api.api_clients import (
    BaseApplicationColocateApiClient,
)
from application_colocations.api.mocks.mock_definitions import (
    ApplicationColocateUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)

BASE_DIR = settings.BASE_DIR


class ApplicationColocateApiClient(BaseApplicationColocateApiClient, MockApiClient):
    endpoint_definition_class = ApplicationColocateUserSpecifiableOpenApiDefinition

    path_to_data = os.path.join(
        BASE_DIR,
        "application_colocations",
        "api",
        "mocks",
        "jsons",
        "data",
        "application_colocations.json",
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "application_colocations", "temp")


class ApplicationColocateColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [r for r in resources if r.get("table_name") == "application_colocate"]
