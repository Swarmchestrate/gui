from application_security_rules.api.definitions import (
    ApplicationSecurityRuleUserSpecifiableOpenApiDefinition,
)
from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)


class BaseApplicationSecurityRuleApiClient(BaseApiClient):
    endpoint = "application_security_rule"


class ApplicationSecurityRuleApiClient(BaseApplicationSecurityRuleApiClient, ApiClient):
    endpoint_definition_class = ApplicationSecurityRuleUserSpecifiableOpenApiDefinition


class ApplicationSecurityRuleColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.application_security_rule",
            }
        )
        return super().get_resources(params=params)
