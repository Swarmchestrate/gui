import os

from django.conf import settings

from editor.api.definitions.mixins import (
    LocalityUserSpecifiableOpenApiDefinitionMixin,
)
from editor.api.mocks.definitions.base import MockUserSpecifiableOpenApiDefinition


class LocalityUserSpecifiableOpenApiDefinition(
    LocalityUserSpecifiableOpenApiDefinitionMixin, MockUserSpecifiableOpenApiDefinition
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "editor",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "locality.json",
    )
