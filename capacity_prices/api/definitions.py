from editor.api.base_definitions import (
    OpenApiDefinition,
    UserSpecifiableOpenApiDefinitionMixin,
)


class CapacityPriceUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "price_id"
    definition_name = "capacity_price"


class CapacityPriceUserSpecifiableOpenApiDefinition(
    OpenApiDefinition, CapacityPriceUserSpecifiableOpenApiDefinitionMixin
):
    pass
