import os

from django.conf import settings

from application_environment_vars.api.definitions import (
    ApplicationEnvironmentVarUserSpecifiableOpenApiDefinitionMixin,
)
from editor.api.mocks.mock_base_definitions import MockUserSpecifiableOpenApiDefinition


class ApplicationEnvironmentVarUserSpecifiableOpenApiDefinition(
    ApplicationEnvironmentVarUserSpecifiableOpenApiDefinitionMixin,
    MockUserSpecifiableOpenApiDefinition,
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "application_environment_vars",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "application_environment_var.json",
    )
