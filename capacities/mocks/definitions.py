import os

from django.conf import settings

from capacities.api.definition_mixins import (
    CapacityUserSpecifiableOpenApiDefinitionMixin,
)
from editor.mocks.definitions import MockUserSpecifiableOpenApiDefinition


class CapacityUserSpecifiableOpenApiDefinition(
    CapacityUserSpecifiableOpenApiDefinitionMixin, MockUserSpecifiableOpenApiDefinition
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "capacities",
        "mocks",
        "jsons",
        "definitions",
        "capacity.json",
    )
