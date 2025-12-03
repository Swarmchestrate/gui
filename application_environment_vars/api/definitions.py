from editor.api.base_definitions import (
    UserSpecifiableOpenApiDefinition,
    UserSpecifiableOpenApiDefinitionMixin,
)


class ApplicationEnvironmentVarUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "id"


class ApplicationEnvironmentVarUserSpecifiableOpenApiDefinition(
    ApplicationEnvironmentVarUserSpecifiableOpenApiDefinitionMixin,
    UserSpecifiableOpenApiDefinition,
):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "application_environment_var"
