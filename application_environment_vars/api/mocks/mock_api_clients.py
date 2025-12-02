import os

from django.conf import settings

from application_environment_vars.api.api_clients import (
    BaseApplicationEnvironmentVarsApiClient,
)
from application_environment_vars.api.mocks.mock_definitions import (
    ApplicationEnvironmentVarsUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)

BASE_DIR = settings.BASE_DIR


class ApplicationEnvironmentVarsApiClient(
    BaseApplicationEnvironmentVarsApiClient, MockApiClient
):
    endpoint_definition_class = (
        ApplicationEnvironmentVarsUserSpecifiableOpenApiDefinition
    )

    path_to_data = os.path.join(
        BASE_DIR,
        "application_environment_vars",
        "api",
        "mocks",
        "jsons",
        "data",
        "application_environment_vars.json",
    )
    path_to_temp_data_dir = os.path.join(
        BASE_DIR, "application_environment_vars", "temp"
    )


class ApplicationEnvironmentVarsColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [
            r for r in resources if r.get("table_name") == "application_environment_var"
        ]
