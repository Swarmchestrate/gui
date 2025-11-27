from editor.api.base_definitions import (
    OpenApiDefinition,
    UserSpecifiableOpenApiDefinitionMixin,
)


class LocalityUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "locality_id"
    definition_name = "locality"


class LocalityUserSpecifiableOpenApiDefinition(
    OpenApiDefinition, LocalityUserSpecifiableOpenApiDefinitionMixin
):
    pass
