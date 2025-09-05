from editor.definitions import UserSpecifiableOpenApiDefinition


class CapacityUserSpecifiableOpenApiDefinition(UserSpecifiableOpenApiDefinition):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = 'capacity'
        self.id_field = 'capacity_id'