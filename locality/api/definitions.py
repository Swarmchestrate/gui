from editor.api.base_definitions import (
    OpenApiDefinition,
    UserSpecifiableOpenApiDefinitionMixin,
)


class LocalityUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "locality_id"


class LocalityUserSpecifiableOpenApiDefinition(
    OpenApiDefinition, LocalityUserSpecifiableOpenApiDefinitionMixin
):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "locality"
