from editor.api.base_definitions import (
    OpenApiDefinition,
    UserSpecifiableOpenApiDefinitionMixin,
)


class CapacityResourceQuotaUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "resource_quota_id"
    definition_name = "capacity_resource_quota"


class CapacityResourceQuotaUserSpecifiableOpenApiDefinition(
    OpenApiDefinition, CapacityResourceQuotaUserSpecifiableOpenApiDefinitionMixin
):
    pass
