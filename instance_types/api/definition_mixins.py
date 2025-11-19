from editor.api.definition_mixins import UserSpecifiableOpenApiDefinitionMixin


class CapacityInstanceTypeUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "id"

    def _get_auto_generated_field_names(self) -> list:
        field_names = super()._get_auto_generated_field_names()
        field_names.append("capacity_id")
        field_names.append("provider")
        return field_names
