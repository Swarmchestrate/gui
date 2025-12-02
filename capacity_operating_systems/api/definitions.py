from editor.api.base_definitions import (
    OpenApiDefinition,
    UserSpecifiableOpenApiDefinitionMixin,
)


class CapacityOperatingSystemUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "id"
    definition_name = "capacity_operating_system"


class CapacityOperatingSystemUserSpecifiableOpenApiDefinition(
    OpenApiDefinition, CapacityOperatingSystemUserSpecifiableOpenApiDefinitionMixin
):
    pass
