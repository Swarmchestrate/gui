from editor.definitions import UserSpecifiableOpenApiDefinition


class InstanceTypeUserSpecifiableOpenApiDefinition(UserSpecifiableOpenApiDefinition):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = 'instance_types'
        self.id_field = 'id'

    @property
    def auto_generated_field_names(self):
        field_names = super().auto_generated_field_names
        field_names.append('provider')
        return field_names
