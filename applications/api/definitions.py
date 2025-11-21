from editor.api.definitions.base import UserSpecifiableOpenApiDefinition


class ApplicationUserSpecifiableOpenApiDefinition(UserSpecifiableOpenApiDefinition):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "application"
        self.id_field = "application_id"
