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


# Applications
class ApplicationApiClient(ApiClient):
    endpoint = "application"
    endpoint_definition_class = ApplicationUserSpecifiableOpenApiDefinition


class ApplicationBehaviourApiClient(ApiClient):
    endpoint = "application_behaviour"
    endpoint_definition_class = ApplicationBehaviourUserSpecifiableOpenApiDefinition


class ApplicationColocateApiClient(ApiClient):
    endpoint = "application_colocate"
    endpoint_definition_class = ApplicationColocateUserSpecifiableOpenApiDefinition


class ApplicationEnvironmentVarApiClient(ApiClient):
    endpoint = "application_environment_var"
    endpoint_definition_class = (
        ApplicationEnvironmentVarUserSpecifiableOpenApiDefinition
    )


class ApplicationPrefResourceProviderApiClient(ApiClient):
    endpoint = "application_pref_resource_provider"
    endpoint_definition_class = (
        ApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition
    )


class ApplicationSecurityRuleApiClient(ApiClient):
    endpoint = "application_security_rule"
    endpoint_definition_class = ApplicationSecurityRuleUserSpecifiableOpenApiDefinition


class ApplicationVolumeApiClient(ApiClient):
    endpoint = "application_volume"
    endpoint_definition_class = ApplicationVolumeUserSpecifiableOpenApiDefinition


# Capacities
class CapacityApiClient(ApiClient):
    endpoint = "capacity"
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition


class CloudCapacityApiClient(CapacityApiClient):
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


class CapacityInstanceTypeApiClient(ApiClient):
    endpoint = "capacity_instance_type"

    def _prepare_update_data(self, data: dict):
        data = super()._prepare_update_data(data)
        data.pop("updated_at", None)
        data.pop(self.endpoint_definition.pk_field_name, None)
        return data

    endpoint_definition_class = CapacityInstanceTypeUserSpecifiableOpenApiDefinition


class CapacityOperatingSystemApiClient(ApiClient):
    endpoint = "capacity_operating_system"
    endpoint_definition_class = CapacityOperatingSystemUserSpecifiableOpenApiDefinition


class CapacityPriceApiClient(ApiClient):
    endpoint = "capacity_price"
    endpoint_definition_class = CapacityPriceUserSpecifiableOpenApiDefinition


class CapacityResourceQuotaApiClient(ApiClient):
    endpoint = "capacity_resource_quota"
    endpoint_definition_class = CapacityResourceQuotaUserSpecifiableOpenApiDefinition


# Localities
class LocalityApiClient(ApiClient):
    endpoint = "locality"
    endpoint_definition_class = LocalityUserSpecifiableOpenApiDefinition


# Column Metadata
class ColumnMetadataApiClient(ApiClient, BaseColumnMetadataApiClient):
    """This class is intended to be subclassed and shouldn't be
    instantiated directly.
    """

    endpoint_definition_class = ColumnMetadataUserSpecifiableOpenApiDefinition

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
