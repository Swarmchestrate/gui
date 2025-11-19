from editor.abc import BaseOpenApiDefinition
from editor.mixins.definition_mixins import UserSpecifiableOpenApiDefinitionMixin


class OpenApiDefinition(BaseOpenApiDefinition):
    openapi_spec: dict
    definition_name: str

    def __init__(self, openapi_spec: dict) -> None:
        self.openapi_spec = openapi_spec

    def _get_definition(self) -> dict:
        return self.openapi_spec.get("definitions", {}).get(self.definition_name, {})


class UserSpecifiableOpenApiDefinition(
    OpenApiDefinition, UserSpecifiableOpenApiDefinitionMixin
):
    pass


class ColumnMetadataUserSpecifiableOpenApiDefinition(UserSpecifiableOpenApiDefinition):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "column_metadata"
        self.id_field = ""
