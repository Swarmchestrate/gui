import os

from django.conf import settings

from application_security_rules.api.definitions import (
    ApplicationSecurityRuleUserSpecifiableOpenApiDefinitionMixin,
)
from editor.api.mocks.mock_base_definitions import MockUserSpecifiableOpenApiDefinition


class ApplicationSecurityRuleUserSpecifiableOpenApiDefinition(
    ApplicationSecurityRuleUserSpecifiableOpenApiDefinitionMixin,
    MockUserSpecifiableOpenApiDefinition,
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "application_security_rules",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "application_security_rule.json",
    )
