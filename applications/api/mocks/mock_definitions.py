import os

from django.conf import settings

from applications.api.definitions import (
    ApplicationMicroserviceUserSpecifiableOpenApiDefinitionMixin,
    ApplicationUserSpecifiableOpenApiDefinitionMixin,
)
from editor.api.mocks.mock_base_definitions import MockUserSpecifiableOpenApiDefinition


class ApplicationUserSpecifiableOpenApiDefinition(
    ApplicationUserSpecifiableOpenApiDefinitionMixin,
    MockUserSpecifiableOpenApiDefinition,
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "applications",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "application.json",
    )


class ApplicationMicroserviceUserSpecifiableOpenApiDefinition(
    ApplicationMicroserviceUserSpecifiableOpenApiDefinitionMixin,
    MockUserSpecifiableOpenApiDefinition,
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "applications",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "application_microservice.json",
    )
