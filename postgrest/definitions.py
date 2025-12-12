from .base.base_definitions import UserSpecifiableOpenApiDefinition


# Applications
class ApplicationUserSpecifiableOpenApiDefinition(UserSpecifiableOpenApiDefinition):
    definition_name = "application_new"


class ApplicationBehaviourUserSpecifiableOpenApiDefinition(
    UserSpecifiableOpenApiDefinition,
):
    definition_name = "application_behaviour"


class ApplicationColocateUserSpecifiableOpenApiDefinition(
    UserSpecifiableOpenApiDefinition,
):
    definition_name = "application_colocate"


class ApplicationEnvironmentVarUserSpecifiableOpenApiDefinition(
    UserSpecifiableOpenApiDefinition,
):
    definition_name = "application_environment_var"


class ApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition(
    UserSpecifiableOpenApiDefinition,
):
    definition_name = "application_pref_resource_provider"


class ApplicationSecurityRuleUserSpecifiableOpenApiDefinition(
    UserSpecifiableOpenApiDefinition,
):
    definition_name = "application_security_rule"


class ApplicationVolumeUserSpecifiableOpenApiDefinition(
    UserSpecifiableOpenApiDefinition,
):
    definition_name = "application_volume"


# Capacities
class CapacityUserSpecifiableOpenApiDefinition(UserSpecifiableOpenApiDefinition):
    definition_name = "capacity"

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


class CapacityEnergyConsumptionUserSpecifiableOpenApiDefinition(
    UserSpecifiableOpenApiDefinition
):
    definition_name = "capacity_energy_consumption"


class CapacityInstanceTypeUserSpecifiableOpenApiDefinition(
    UserSpecifiableOpenApiDefinition,
):
    definition_name = "capacity_instance_type"

    def _get_auto_generated_field_names(self) -> list:
        field_names = super()._get_auto_generated_field_names()
        field_names.append("capacity_id")
        field_names.append("provider")
        return field_names


class CapacityOperatingSystemUserSpecifiableOpenApiDefinition(
    UserSpecifiableOpenApiDefinition
):
    definition_name = "capacity_operating_system"


class CapacityPriceUserSpecifiableOpenApiDefinition(UserSpecifiableOpenApiDefinition):
    definition_name = "capacity_price"


class CapacityResourceQuotaUserSpecifiableOpenApiDefinition(
    UserSpecifiableOpenApiDefinition
):
    definition_name = "capacity_resource_quota"


# Localities
class LocalityUserSpecifiableOpenApiDefinition(UserSpecifiableOpenApiDefinition):
    definition_name = "locality"


# Column metadata
class ColumnMetadataUserSpecifiableOpenApiDefinition(UserSpecifiableOpenApiDefinition):
    definition_name = "column_metadata"
