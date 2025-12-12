from .base.mock_base_definitions import MockUserSpecifiableOpenApiDefinition


# Applications
class MockApplicationUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application"


class MockApplicationMicroserviceUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application_microservice"


class MockApplicationBehaviourUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application_behaviour"


class MockApplicationColocateUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application_colocate"


class MockApplicationEnvironmentVarUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application_environment_var"


class MockApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application_pref_resource_provider"


class MockApplicationSecurityRuleUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application_security_rule"


class MockApplicationVolumeUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "application_volume"


# Capacities
class MockCapacityUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition
):
    definition_name = "capacity"


class MockCapacityEnergyConsumptionUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "capacity_energy_consumption"


class MockCapacityInstanceTypeUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "capacity_instance_type"


class MockCapacityOperatingSystemUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "capacity_operating_system"


class MockCapacityPriceUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "capacity_price"


class MockCapacityResourceQuotaUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition,
):
    definition_name = "capacity_resource_quota"


# Localities
class MockLocalityUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition
):
    definition_name = "locality"


# Column Metadata
class MockColumnMetadataUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition
):
    definition_name = "column_metadata"
