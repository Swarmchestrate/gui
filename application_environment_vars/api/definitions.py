from editor.api.base_definitions import (
    UserSpecifiableOpenApiDefinition,
    UserSpecifiableOpenApiDefinitionMixin,
)


class ApplicationEnvironmentVarUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "id"
    definition_name = "application_environment_var"


class ApplicationEnvironmentVarUserSpecifiableOpenApiDefinition(
    ApplicationEnvironmentVarUserSpecifiableOpenApiDefinitionMixin,
    UserSpecifiableOpenApiDefinition,
):
    pass
