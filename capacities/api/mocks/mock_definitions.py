import os

from django.conf import settings

from capacities.api.definitions import (
    CapacityUserSpecifiableOpenApiDefinitionMixin,
)
from editor.api.mocks.mock_base_definitions import MockUserSpecifiableOpenApiDefinition


class CapacityUserSpecifiableOpenApiDefinition(
    CapacityUserSpecifiableOpenApiDefinitionMixin, MockUserSpecifiableOpenApiDefinition
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "capacities",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "capacity.json",
    )
