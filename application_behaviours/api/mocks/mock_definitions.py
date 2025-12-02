import os

from django.conf import settings

from application_behaviours.api.definitions import (
    ApplicationBehaviourUserSpecifiableOpenApiDefinitionMixin,
)
from editor.api.mocks.mock_base_definitions import MockUserSpecifiableOpenApiDefinition


class ApplicationBehaviourUserSpecifiableOpenApiDefinition(
    ApplicationBehaviourUserSpecifiableOpenApiDefinitionMixin,
    MockUserSpecifiableOpenApiDefinition,
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "application_behaviours",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "application_behaviour.json",
    )
