class OpenApiDefinition:
    openapi_spec: dict
    definition_name: str
    id_field: str

    def __init__(self, openapi_spec: dict) -> None:
        self.openapi_spec = openapi_spec
        self.definition_name = None
        self.id_field = None

    # Non-public methods
    def _get_definition(self) -> dict:
        return (self.openapi_spec
                .get('definitions', {})
                .get(self.definition_name, {}))

    def _get_required_field_names(self):
        return self._get_definition().get('required', list())

    def _get_all_fields(self) -> dict:
        return self._get_definition().get('properties', {})

    def _get_fields_with_names(self, names: list[str]):
        all_fields = self._get_all_fields()
        return {
            key: value
            for key, value in all_fields.items()
            if key in names
        }


class UserSpecifiableOpenApiDefinition(OpenApiDefinition):
    # Properties
    @property
    def auto_generated_field_names(self):
        return list([self.id_field])

    # Non-public methods
    def _get_all_user_specifiable_fields(self):
        all_fields = self._get_all_fields()
        return {
            key: value
            for key, value in all_fields.items()
            if value.get('name') not in self.auto_generated_field_names
        }

    def _get_required_user_specifiable_field_names(self):
        required_field_names = set(self._get_required_field_names())
        auto_generated_field_names = set(self.auto_generated_field_names)
        return list(required_field_names - auto_generated_field_names)

    # Public methods
    def get_all_user_specifiable_fields(self):
        return self._get_all_user_specifiable_fields()

    def get_user_specifiable_field_formats(self):
        all_fields = self._get_all_fields()
        return list(set(
            value.get('format')
            for key, value in all_fields.items()
            if key not in self.auto_generated_field_names 
        ))

    def get_user_specifiable_fields_with_format(self, format: str):
        all_user_specifiable_fields = self._get_all_user_specifiable_fields()
        return {
            key: value
            for key, value in all_user_specifiable_fields.items()
            if value.get('format') == format
        }

    def get_required_user_specifiable_fields(self):
        field_names = self._get_required_user_specifiable_field_names()
        return self._get_fields_with_names(field_names)