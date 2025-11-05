from editor.definitions import UserSpecifiableOpenApiDefinition


class InstanceTypeUserSpecifiableOpenApiDefinition(UserSpecifiableOpenApiDefinition):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = 'instance_types'
        self.id_field = 'id'

    def _get_auto_generated_field_names(self) -> list:
        field_names = super()._get_auto_generated_field_names()
        field_names.append('provider')
        return field_names
