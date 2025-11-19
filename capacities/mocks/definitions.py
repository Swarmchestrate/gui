import os

from django.conf import settings

from editor.mocks.definitions import MockUserSpecifiableOpenApiDefinition

from ..mixins.definition_mixins import CapacityUserSpecifiableOpenApiDefinitionMixin


class CapacityUserSpecifiableOpenApiDefinition(
    CapacityUserSpecifiableOpenApiDefinitionMixin, MockUserSpecifiableOpenApiDefinition
):
    path_to_definition = os.path.join(
        settings.BASE_DIR, "capacities", "mocks", "definitions", "capacity.json"
    )
