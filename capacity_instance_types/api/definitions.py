from editor.api.base_definitions import (
    UserSpecifiableOpenApiDefinition,
    UserSpecifiableOpenApiDefinitionMixin,
)


class CapacityInstanceTypeUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "id"

    def _get_auto_generated_field_names(self) -> list:
        field_names = super()._get_auto_generated_field_names()
        field_names.append("capacity_id")
        field_names.append("provider")
        return field_names


class InstanceTypeUserSpecifiableOpenApiDefinition(
    CapacityInstanceTypeUserSpecifiableOpenApiDefinitionMixin,
    UserSpecifiableOpenApiDefinition,
):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "capacity_instance_type"


class CapacityInstanceTypeUserSpecifiableOpenApiDefinition(
    CapacityInstanceTypeUserSpecifiableOpenApiDefinitionMixin,
    UserSpecifiableOpenApiDefinition,
):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "capacity_instance_type"
