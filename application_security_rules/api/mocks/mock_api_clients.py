import os

from django.conf import settings

from application_security_rules.api.api_clients import (
    BaseApplicationSecurityRuleApiClient,
)
from application_security_rules.api.mocks.mock_definitions import (
    ApplicationSecurityRuleUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)

BASE_DIR = settings.BASE_DIR


class ApplicationSecurityRuleApiClient(
    BaseApplicationSecurityRuleApiClient, MockApiClient
):
    endpoint_definition_class = ApplicationSecurityRuleUserSpecifiableOpenApiDefinition

    path_to_data = os.path.join(
        BASE_DIR,
        "application_security_rules",
        "api",
        "mocks",
        "jsons",
        "data",
        "application_security_rules.json",
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "application_security_rules", "temp")


class ApplicationSecurityRuleColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [
            r for r in resources if r.get("table_name") == "application_security_rule"
        ]
