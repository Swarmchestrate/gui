from ast import literal_eval as make_tuple

from .base.base_api_clients import ApiClient, BaseColumnMetadataApiClient
from .definitions import (
    ApplicationBehaviourUserSpecifiableOpenApiDefinition,
    ApplicationColocateUserSpecifiableOpenApiDefinition,
    ApplicationEnvironmentVarUserSpecifiableOpenApiDefinition,
    ApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition,
    ApplicationSecurityRuleUserSpecifiableOpenApiDefinition,
    ApplicationUserSpecifiableOpenApiDefinition,
    ApplicationVolumeUserSpecifiableOpenApiDefinition,
    CapacityEnergyConsumptionUserSpecifiableOpenApiDefinition,
    CapacityInstanceTypeUserSpecifiableOpenApiDefinition,
    CapacityOperatingSystemUserSpecifiableOpenApiDefinition,
    CapacityPriceUserSpecifiableOpenApiDefinition,
    CapacityResourceQuotaUserSpecifiableOpenApiDefinition,
    CapacityUserSpecifiableOpenApiDefinition,
    ColumnMetadataUserSpecifiableOpenApiDefinition,
    LocalityUserSpecifiableOpenApiDefinition,
)
from .readable_text_utils import (
    application_behaviour_type_readable,
    application_behaviour_type_readable_plural,
    application_colocate_type_readable,
    application_colocate_type_readable_plural,
    application_environment_var_type_readable,
    application_environment_var_type_readable_plural,
    application_pref_resource_provider_type_readable,
    application_pref_resource_provider_type_readable_plural,
    application_security_rule_type_readable,
    application_security_rule_type_readable_plural,
    application_type_readable,
    application_type_readable_plural,
    application_volume_type_readable,
    application_volume_type_readable_plural,
    capacity_energy_consumption_type_readable,
    capacity_energy_consumption_type_readable_plural,
    capacity_instance_type_type_readable,
    capacity_instance_type_type_readable_plural,
    capacity_operating_system_type_readable,
    capacity_operating_system_type_readable_plural,
    capacity_price_type_readable,
    capacity_price_type_readable_plural,
    capacity_resource_quota_type_readable,
    capacity_resource_quota_type_readable_plural,
    capacity_type_readable,
    capacity_type_readable_plural,
    cloud_capacity_type_readable,
    cloud_capacity_type_readable_plural,
    edge_capacity_type_readable,
    edge_capacity_type_readable_plural,
    locality_type_readable,
    locality_type_readable_plural,
)


# Applications
class ApplicationApiClient(ApiClient):
    endpoint = "application"
    endpoint_definition_class = ApplicationUserSpecifiableOpenApiDefinition
    type_readable = application_type_readable()
    type_readable_plural = application_type_readable_plural()

    def update(self, resource_id: int, data: dict):
        data = self._set_updated_at_to_now(data)
        return super().update(resource_id, data)


class ApplicationBehaviourApiClient(ApiClient):
    endpoint = "application_behaviour"
    endpoint_definition_class = ApplicationBehaviourUserSpecifiableOpenApiDefinition
    type_readable = application_behaviour_type_readable()
    type_readable_plural = application_behaviour_type_readable_plural()


class ApplicationColocateApiClient(ApiClient):
    endpoint = "application_colocate"
    endpoint_definition_class = ApplicationColocateUserSpecifiableOpenApiDefinition
    type_readable = application_colocate_type_readable()
    type_readable_plural = application_colocate_type_readable_plural()


class ApplicationEnvironmentVarApiClient(ApiClient):
    endpoint = "application_environment_var"
    endpoint_definition_class = (
        ApplicationEnvironmentVarUserSpecifiableOpenApiDefinition
    )
    type_readable = application_environment_var_type_readable()
    type_readable_plural = application_environment_var_type_readable_plural()


class ApplicationPrefResourceProviderApiClient(ApiClient):
    endpoint = "application_pref_resource_provider"
    endpoint_definition_class = (
        ApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition
    )
    type_readable = application_pref_resource_provider_type_readable()
    type_readable_plural = application_pref_resource_provider_type_readable_plural()


class ApplicationSecurityRuleApiClient(ApiClient):
    endpoint = "application_security_rule"
    endpoint_definition_class = ApplicationSecurityRuleUserSpecifiableOpenApiDefinition
    type_readable = application_security_rule_type_readable()
    type_readable_plural = application_security_rule_type_readable_plural()


class ApplicationVolumeApiClient(ApiClient):
    endpoint = "application_volume"
    endpoint_definition_class = ApplicationVolumeUserSpecifiableOpenApiDefinition
    type_readable = application_volume_type_readable()
    type_readable_plural = application_volume_type_readable_plural()


# Capacities
class CapacityApiClient(ApiClient):
    endpoint = "capacity"
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition
    type_readable = capacity_type_readable()
    type_readable_plural = capacity_type_readable_plural()

    def update(self, resource_id: int, data: dict):
        data = self._set_updated_at_to_now(data)
        return super().update(resource_id, data)


class CloudCapacityApiClient(CapacityApiClient):
    type_readable = cloud_capacity_type_readable()
    type_readable_plural = cloud_capacity_type_readable_plural()

    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update({"resource_type": "eq.Cloud"})
        return super().get_resources(params=params)

    def register(self, data: dict):
        data.update({"resource_type": "Cloud"})
        return super().register(data)

    def delete(self, resource_id: int, params: dict | None = None):
        if not params:
            params = dict()
        params.update({"resource_type": "eq.Cloud"})
        return super().delete(resource_id, params)


class EdgeCapacityApiClient(CapacityApiClient):
    type_readable = edge_capacity_type_readable()
    type_readable_plural = edge_capacity_type_readable_plural()

    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update({"resource_type": "eq.Edge"})
        return super().get_resources(params)

    def register(self, data: dict):
        data.update({"resource_type": "Edge"})
        return super().register(data)

    def delete(self, resource_id: int, params: dict | None = None):
        if not params:
            params = dict()
        params.update({"resource_type": "eq.Edge"})
        return super().delete(resource_id, params)


class CapacityEnergyConsumptionApiClient(ApiClient):
    endpoint = "capacity_energy_consumption"
    endpoint_definition_class = (
        CapacityEnergyConsumptionUserSpecifiableOpenApiDefinition
    )
    type_readable = capacity_energy_consumption_type_readable()
    type_readable_plural = capacity_energy_consumption_type_readable_plural()


class CapacityInstanceTypeApiClient(ApiClient):
    endpoint = "capacity_instance_type"
    type_readable = capacity_instance_type_type_readable()
    type_readable_plural = capacity_instance_type_type_readable_plural()

    endpoint_definition_class = CapacityInstanceTypeUserSpecifiableOpenApiDefinition


class CapacityOperatingSystemApiClient(ApiClient):
    endpoint = "capacity_operating_system"
    endpoint_definition_class = CapacityOperatingSystemUserSpecifiableOpenApiDefinition
    type_readable = capacity_operating_system_type_readable()
    type_readable_plural = capacity_operating_system_type_readable_plural()


class CapacityPriceApiClient(ApiClient):
    endpoint = "capacity_price"
    endpoint_definition_class = CapacityPriceUserSpecifiableOpenApiDefinition
    type_readable = capacity_price_type_readable()
    type_readable_plural = capacity_price_type_readable_plural()


class CapacityResourceQuotaApiClient(ApiClient):
    endpoint = "capacity_resource_quota"
    endpoint_definition_class = CapacityResourceQuotaUserSpecifiableOpenApiDefinition
    type_readable = capacity_resource_quota_type_readable()
    type_readable_plural = capacity_resource_quota_type_readable_plural()


# Localities
class LocalityApiClient(ApiClient):
    endpoint = "locality"
    endpoint_definition_class = LocalityUserSpecifiableOpenApiDefinition
    type_readable = locality_type_readable()
    type_readable_plural = locality_type_readable_plural()


# Column Metadata
class ColumnMetadataApiClient(ApiClient, BaseColumnMetadataApiClient):
    """This class is intended to be subclassed and shouldn't be
    instantiated directly.
    """

    endpoint_definition_class = ColumnMetadataUserSpecifiableOpenApiDefinition
    type_readable = "column metadata"
    type_readable_plural = "column metadata"

    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        if not self.disabled_categories:
            return self._get_resources(params)
        and_conditions = set(
            f"category.neq.{category}" for category in self.disabled_categories
        )
        if "and" in params:
            existing_and_conditions = make_tuple(params.get("and", "()"))
            for condition in existing_and_conditions:
                and_conditions.add(condition)
        if "category" in params:
            and_conditions.add(f"category.{params.get('category')}")
            params.pop("category", None)
        params.update(
            {
                "and": f"({','.join(and_conditions)})",
            }
        )
        return self._get_resources(params)

    def get_resources_by_category(self, category: str):
        return self.get_resources(params={"category": f"eq.{category}"})

    def get_by_table_name(self, table_name: str):
        return self.get_resources(params={"table_name": f"eq.{table_name}"})

    def get_resources_for_disabled_categories(self):
        resources = self._get_resources()
        return [r for r in resources if r.get("category") in self.disabled_categories]


class ApplicationColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update({"table_name": "eq.application"})
        return super().get_resources(params)


class ApplicationMicroserviceColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update({"table_name": "eq.application_microservice"})
        return super().get_resources(params)


class CloudCapacityColumnMetadataApiClient(ColumnMetadataApiClient):
    disabled_categories = ["Edge Specific", "Networking"]

    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update({"table_name": "eq.capacity"})
        return super().get_resources(params)


class EdgeCapacityColumnMetadataApiClient(ColumnMetadataApiClient):
    disabled_categories = ["System Specific"]

    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update({"table_name": "eq.capacity"})
        return super().get_resources(params)
