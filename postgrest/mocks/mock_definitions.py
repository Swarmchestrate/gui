from .base.mock_base_definitions import MockUserSpecifiableOpenApiDefinition


# Applications
class ApplicationUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application"


class ApplicationMicroserviceUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application_microservice"


class ApplicationBehaviourUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application_behaviour"


class ApplicationColocateUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application_colocation"


class ApplicationEnvironmentVarUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application_environment_var"


class ApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application_pref_resource_provider"


class ApplicationSecurityRuleUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application_security_rule"


class ApplicationVolumeUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application_volume"


# Capacities
class CapacityUserSpecifiableOpenApiDefinition(MockUserSpecifiableOpenApiDefinition):
    definition_name = "capacity"


class CapacityEnergyConsumptionUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "capacity_energy_consumption"


class CapacityInstanceTypeUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "capacity_instance_type"


class CapacityOperatingSystemUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "capacity_operating_system"


class CapacityPriceUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "capacity_price"


class CapacityResourceQuotaUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "capacity_resource_quota"


# Localities
class LocalityUserSpecifiableOpenApiDefinition(MockUserSpecifiableOpenApiDefinition):
    definition_name = "locality"


# Column Metadata
class MockColumnMetadataUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition
):
    definition_name = "column_metadata"
