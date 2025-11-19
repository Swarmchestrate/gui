import os

from django.conf import settings

from editor.mocks.definitions import MockUserSpecifiableOpenApiDefinition

from ..definition_mixins import (
    CapacityInstanceTypeUserSpecifiableOpenApiDefinitionMixin,
)


class CapacityInstanceTypeUserSpecifiableOpenApiDefinition(
    CapacityInstanceTypeUserSpecifiableOpenApiDefinitionMixin,
    MockUserSpecifiableOpenApiDefinition,
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "instance_types",
        "mocks",
        "data",
        "definitions",
        "capacity_instance_type.json",
    )
