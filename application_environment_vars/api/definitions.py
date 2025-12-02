from editor.api.base_definitions import (
    UserSpecifiableOpenApiDefinition,
    UserSpecifiableOpenApiDefinitionMixin,
)


class ApplicationEnvironmentVarsUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "id"


class InstanceTypeUserSpecifiableOpenApiDefinition(
    ApplicationEnvironmentVarsUserSpecifiableOpenApiDefinitionMixin,
    UserSpecifiableOpenApiDefinition,
):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "application_environment_var"


class ApplicationEnvironmentVarsUserSpecifiableOpenApiDefinition(
    ApplicationEnvironmentVarsUserSpecifiableOpenApiDefinitionMixin,
    UserSpecifiableOpenApiDefinition,
):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "application_environment_var"
