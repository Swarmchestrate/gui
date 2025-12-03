import os

from django.conf import settings

from application_pref_resource_providers.api.api_clients import (
    BaseApplicationPrefResourceProviderApiClient,
)
from application_pref_resource_providers.api.mocks.mock_definitions import (
    ApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)

BASE_DIR = settings.BASE_DIR


class ApplicationPrefResourceProviderApiClient(
    BaseApplicationPrefResourceProviderApiClient, MockApiClient
):
    endpoint_definition_class = (
        ApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition
    )

    path_to_data = os.path.join(
        BASE_DIR,
        "application_pref_resource_providers",
        "api",
        "mocks",
        "jsons",
        "data",
        "application_pref_resource_providers.json",
    )
    path_to_temp_data_dir = os.path.join(
        BASE_DIR, "application_pref_resource_providers", "temp"
    )


class ApplicationPrefResourceProviderColumnMetadataApiClient(
    MockColumnMetadataApiClient
):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [
            r
            for r in resources
            if r.get("table_name") == "application_pref_resource_provider"
        ]
