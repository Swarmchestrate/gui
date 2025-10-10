from editor.definitions import UserSpecifiableOpenApiDefinition


class InstanceTypeUserSpecifiableOpenApiDefinition(UserSpecifiableOpenApiDefinition):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = 'instance_types'
        self.id_field = 'id'
