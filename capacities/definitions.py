from editor.definitions import OpenApiDefinition

from .mixins.definition_mixins import CapacityUserSpecifiableOpenApiDefinitionMixin


class CapacityUserSpecifiableOpenApiDefinition(
    OpenApiDefinition, CapacityUserSpecifiableOpenApiDefinitionMixin
):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "capacity"
