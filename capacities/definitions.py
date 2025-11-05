from editor.definitions import UserSpecifiableOpenApiDefinition


class CapacityUserSpecifiableOpenApiDefinition(UserSpecifiableOpenApiDefinition):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = 'capacity'
        self.id_field = 'capacity_id'

    def _get_auto_generated_field_names(self) -> list:
        names = super()._get_auto_generated_field_names()
        names.append('resource_type')
        return names

    def _get_disabled_field_names(self) -> list:
        names = super()._get_disabled_field_names()
        names.extend([
            'price',
            'trust',
            'energy_consumption',
        ])
        return names
