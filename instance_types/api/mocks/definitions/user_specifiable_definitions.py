import os

from django.conf import settings

from editor.api.mocks.definitions.base import MockUserSpecifiableOpenApiDefinition
from instance_types.api.definitions.mixins import (
    CapacityInstanceTypeUserSpecifiableOpenApiDefinitionMixin,
)


class CapacityInstanceTypeUserSpecifiableOpenApiDefinition(
    CapacityInstanceTypeUserSpecifiableOpenApiDefinitionMixin,
    MockUserSpecifiableOpenApiDefinition,
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "instance_types",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "capacity_instance_type.json",
    )
