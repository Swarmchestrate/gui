from editor.api.definition_mixins import UserSpecifiableOpenApiDefinitionMixin


class CapacityUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "capacity_id"

    def _get_auto_generated_field_names(self) -> list:
        names = super()._get_auto_generated_field_names()
        names.append("resource_type")
        return names

    def _get_disabled_field_names(self) -> list:
        names = super()._get_disabled_field_names()
        names.extend(
            [
                "price",
                "trust",
                "energy_consumption",
                "instance_quota",
            ]
        )
        return names
