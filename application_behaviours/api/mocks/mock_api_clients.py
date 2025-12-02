import os

from django.conf import settings

from application_behaviours.api.api_clients import BaseApplicationBehaviourApiClient
from application_behaviours.api.mocks.mock_definitions import (
    ApplicationBehaviourUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)

BASE_DIR = settings.BASE_DIR


class ApplicationBehaviourApiClient(BaseApplicationBehaviourApiClient, MockApiClient):
    endpoint_definition_class = ApplicationBehaviourUserSpecifiableOpenApiDefinition

    path_to_data = os.path.join(
        BASE_DIR,
        "application_behaviours",
        "api",
        "mocks",
        "jsons",
        "data",
        "application_behaviours.json",
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "application_behaviours", "temp")


class ApplicationBehaviourColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [r for r in resources if r.get("table_name") == "application_behaviour"]
