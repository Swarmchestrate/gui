from editor.api.definitions import UserSpecifiableOpenApiDefinition

from .definition_mixins import CapacityInstanceTypeUserSpecifiableOpenApiDefinitionMixin


class InstanceTypeUserSpecifiableOpenApiDefinition(
    CapacityInstanceTypeUserSpecifiableOpenApiDefinitionMixin,
    UserSpecifiableOpenApiDefinition,
):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "instance_type"


class CapacityInstanceTypeUserSpecifiableOpenApiDefinition(
    CapacityInstanceTypeUserSpecifiableOpenApiDefinitionMixin,
    UserSpecifiableOpenApiDefinition,
):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "capacity_instance_type"
