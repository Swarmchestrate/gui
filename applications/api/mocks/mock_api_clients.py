import os

from django.conf import settings

from applications.api.api_clients import (
    BaseApplicationApiClient,
    BaseApplicationMicroserviceApiClient,
)
from applications.api.mocks.mock_definitions import (
    ApplicationMicroserviceUserSpecifiableOpenApiDefinition,
    ApplicationUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)

BASE_DIR = settings.BASE_DIR


class ApplicationApiClient(BaseApplicationApiClient, MockApiClient):
    endpoint_definition_class = ApplicationUserSpecifiableOpenApiDefinition

    path_to_data = os.path.join(
        BASE_DIR,
        "applications",
        "api",
        "mocks",
        "jsons",
        "data",
        "applications.json",
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "applications", "temp")


class ApplicationColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [r for r in resources if r.get("table_name") == "application"]


class ApplicationMicroserviceApiClient(
    BaseApplicationMicroserviceApiClient, MockApiClient
):
    endpoint_definition_class = ApplicationMicroserviceUserSpecifiableOpenApiDefinition

    path_to_data = os.path.join(
        BASE_DIR,
        "applications",
        "api",
        "mocks",
        "jsons",
        "data",
        "application_microservices.json",
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "applications", "temp")


class ApplicationMicroserviceColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [
            r for r in resources if r.get("table_name") == "application_microservice"
        ]
