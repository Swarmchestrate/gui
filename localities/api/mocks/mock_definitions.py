import os

from django.conf import settings

from editor.api.mocks.mock_base_definitions import MockUserSpecifiableOpenApiDefinition
from localities.api.definitions import (
    LocalityUserSpecifiableOpenApiDefinitionMixin,
)


class LocalityUserSpecifiableOpenApiDefinition(
    LocalityUserSpecifiableOpenApiDefinitionMixin, MockUserSpecifiableOpenApiDefinition
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "localities",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "locality.json",
    )
