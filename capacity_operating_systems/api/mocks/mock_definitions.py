import os

from django.conf import settings

from capacity_operating_systems.api.definitions import (
    CapacityOperatingSystemUserSpecifiableOpenApiDefinitionMixin,
)
from editor.api.mocks.mock_base_definitions import MockUserSpecifiableOpenApiDefinition


class CapacityOperatingSystemUserSpecifiableOpenApiDefinition(
    CapacityOperatingSystemUserSpecifiableOpenApiDefinitionMixin,
    MockUserSpecifiableOpenApiDefinition,
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "capacity_operating_systems",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "capacity_operating_system.json",
    )
