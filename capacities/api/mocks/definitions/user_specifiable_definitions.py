import os

from django.conf import settings

from capacities.api.definitions.mixins import (
    CapacityUserSpecifiableOpenApiDefinitionMixin,
)
from editor.api.mocks.definitions.base import MockUserSpecifiableOpenApiDefinition


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
