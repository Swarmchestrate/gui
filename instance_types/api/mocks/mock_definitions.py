import os

from django.conf import settings

from editor.api.mocks.mock_base_definitions import MockUserSpecifiableOpenApiDefinition
from instance_types.api.definitions import (
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
