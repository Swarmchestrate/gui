import os

from django.conf import settings

from application_colocations.api.definitions import (
    ApplicationColocateUserSpecifiableOpenApiDefinitionMixin,
)
from editor.api.mocks.mock_base_definitions import MockUserSpecifiableOpenApiDefinition


class ApplicationColocateUserSpecifiableOpenApiDefinition(
    ApplicationColocateUserSpecifiableOpenApiDefinitionMixin,
    MockUserSpecifiableOpenApiDefinition,
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "application_colocations",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "application_colocate.json",
    )
