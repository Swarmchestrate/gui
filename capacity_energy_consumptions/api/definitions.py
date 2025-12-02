from editor.api.base_definitions import (
    OpenApiDefinition,
    UserSpecifiableOpenApiDefinitionMixin,
)


class CapacityEnergyConsumptionUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "energy_consumption_id"
    definition_name = "capacity_energy_consumption"


class CapacityEnergyConsumptionUserSpecifiableOpenApiDefinition(
    OpenApiDefinition, CapacityEnergyConsumptionUserSpecifiableOpenApiDefinitionMixin
):
    pass
