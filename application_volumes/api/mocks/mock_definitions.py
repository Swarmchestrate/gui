import os

from django.conf import settings

from application_volumes.api.definitions import (
    ApplicationVolumeUserSpecifiableOpenApiDefinitionMixin,
)
from editor.api.mocks.mock_base_definitions import MockUserSpecifiableOpenApiDefinition


class ApplicationVolumeUserSpecifiableOpenApiDefinition(
    ApplicationVolumeUserSpecifiableOpenApiDefinitionMixin,
    MockUserSpecifiableOpenApiDefinition,
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "application_volumes",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "application_volume.json",
    )
