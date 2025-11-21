from editor.api.definitions.base import OpenApiDefinition

from .mixins import CapacityUserSpecifiableOpenApiDefinitionMixin


class CapacityUserSpecifiableOpenApiDefinition(
    OpenApiDefinition, CapacityUserSpecifiableOpenApiDefinitionMixin
):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "capacity"
