import os

from django.conf import settings

from postgrest.base.base_api_clients import BaseColumnMetadataApiClient
from postgrest.mocks.base.mock_base_api_clients import MockApiClient
from postgrest.mocks.mock_definitions import (
    MockColumnMetadataUserSpecifiableOpenApiDefinition,
)
from postgrest.readable_text_utils import (
    application_behaviour_type_readable,
    application_behaviour_type_readable_plural,
    application_colocate_type_readable,
    application_colocate_type_readable_plural,
    application_environment_var_type_readable,
    application_environment_var_type_readable_plural,
    application_microservice_type_readable,
    application_microservice_type_readable_plural,
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
    cloud_capacity_type_readable,
    cloud_capacity_type_readable_plural,
    edge_capacity_type_readable,
    edge_capacity_type_readable_plural,
    locality_type_readable,
    locality_type_readable_plural,
)

from .mock_definitions import (
    MockApplicationBehaviourUserSpecifiableOpenApiDefinition,
    MockApplicationColocateUserSpecifiableOpenApiDefinition,
    MockApplicationEnvironmentVarUserSpecifiableOpenApiDefinition,
    MockApplicationMicroserviceUserSpecifiableOpenApiDefinition,
    MockApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition,
    MockApplicationSecurityRuleUserSpecifiableOpenApiDefinition,
    MockApplicationUserSpecifiableOpenApiDefinition,
    MockApplicationVolumeUserSpecifiableOpenApiDefinition,
    MockCapacityEnergyConsumptionUserSpecifiableOpenApiDefinition,
    MockCapacityInstanceTypeUserSpecifiableOpenApiDefinition,
    MockCapacityOperatingSystemUserSpecifiableOpenApiDefinition,
    MockCapacityPriceUserSpecifiableOpenApiDefinition,
    MockCapacityResourceQuotaUserSpecifiableOpenApiDefinition,
    MockCapacityUserSpecifiableOpenApiDefinition,
    MockLocalityUserSpecifiableOpenApiDefinition,
)

BASE_DIR = settings.BASE_DIR


# Applications
class MockApplicationApiClient(MockApiClient):
    endpoint = "application"
    endpoint_definition_class = MockApplicationUserSpecifiableOpenApiDefinition
    type_readable = application_type_readable()
    type_readable_plural = application_type_readable_plural()

    def update(self, resource_id: int, data: dict):
        data = self._set_updated_at_to_now(data)
        return super().update(resource_id, data)


class MockApplicationMicroserviceApiClient(MockApiClient):
    endpoint = "application_microservice"
    endpoint_definition_class = (
        MockApplicationMicroserviceUserSpecifiableOpenApiDefinition
    )
    type_readable = application_microservice_type_readable()
    type_readable = application_microservice_type_readable_plural()


class MockApplicationBehaviourApiClient(MockApiClient):
    endpoint = "application_behaviour"
    endpoint_definition_class = MockApplicationBehaviourUserSpecifiableOpenApiDefinition
    type_readable = application_behaviour_type_readable()
    type_readable_plural = application_behaviour_type_readable_plural()


class MockApplicationColocateApiClient(MockApiClient):
    endpoint = "application_colocate"
    endpoint_definition_class = MockApplicationColocateUserSpecifiableOpenApiDefinition
    type_readable = application_colocate_type_readable()
    type_readable_plural = application_colocate_type_readable_plural()


class MockApplicationEnvironmentVarApiClient(MockApiClient):
    endpoint = "application_environment_var"
    endpoint_definition_class = (
        MockApplicationEnvironmentVarUserSpecifiableOpenApiDefinition
    )
    type_readable = application_environment_var_type_readable()
    type_readable_plural = application_environment_var_type_readable_plural()


class MockApplicationPrefResourceProviderApiClient(MockApiClient):
    endpoint = "application_pref_resource_provider"
    endpoint_definition_class = (
        MockApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition
    )
    type_readable = application_pref_resource_provider_type_readable()
    type_readable_plural = application_pref_resource_provider_type_readable_plural()


class MockApplicationSecurityRuleApiClient(MockApiClient):
    endpoint = "application_security_rule"
    endpoint_definition_class = (
        MockApplicationSecurityRuleUserSpecifiableOpenApiDefinition
    )
    type_readable = application_security_rule_type_readable()
    type_readable_plural = application_security_rule_type_readable_plural()


class MockApplicationVolumeApiClient(MockApiClient):
    endpoint = "application_volume"
    endpoint_definition_class = MockApplicationVolumeUserSpecifiableOpenApiDefinition
    type_readable = application_volume_type_readable()
    type_readable_plural = application_volume_type_readable_plural()


# Capacities
class MockCloudCapacityApiClient(MockApiClient):
    endpoint = "capacity"
    endpoint_definition_class = MockCapacityUserSpecifiableOpenApiDefinition
    type_readable = cloud_capacity_type_readable()
    type_readable_plural = cloud_capacity_type_readable_plural()

    @property
    def path_to_data(self):
        return os.path.join(self.path_to_data_dir, "cloud_capacity.json")

    @property
    def path_to_temp_data(self):
        return os.path.join(self.path_to_temp_data_dir, "cloud_capacity.json")

    def update(self, resource_id: int, data: dict):
        data = self._set_updated_at_to_now(data)
        return super().update(resource_id, data)


class MockEdgeCapacityApiClient(MockApiClient):
    endpoint = "capacity"
    endpoint_definition_class = MockCapacityUserSpecifiableOpenApiDefinition
    type_readable = edge_capacity_type_readable()
    type_readable_plural = edge_capacity_type_readable_plural()

    @property
    def path_to_data(self):
        return os.path.join(self.path_to_data_dir, "edge_capacity.json")

    @property
    def path_to_temp_data(self):
        return os.path.join(self.path_to_temp_data_dir, "edge_capacity.json")

    def update(self, resource_id: int, data: dict):
        data = self._set_updated_at_to_now(data)
        return super().update(resource_id, data)


class MockCapacityEnergyConsumptionApiClient(MockApiClient):
    endpoint = "capacity_energy_consumption"
    endpoint_definition_class = (
        MockCapacityEnergyConsumptionUserSpecifiableOpenApiDefinition
    )
    type_readable = capacity_energy_consumption_type_readable()
    type_readable_plural = capacity_energy_consumption_type_readable_plural()


class MockCapacityInstanceTypeApiClient(MockApiClient):
    endpoint = "capacity_instance_type"
    endpoint_definition_class = MockCapacityInstanceTypeUserSpecifiableOpenApiDefinition
    type_readable = capacity_instance_type_type_readable()
    type_readable_plural = capacity_instance_type_type_readable_plural()


class MockCapacityOperatingSystemApiClient(MockApiClient):
    endpoint = "capacity_operating_system"
    endpoint_definition_class = (
        MockCapacityOperatingSystemUserSpecifiableOpenApiDefinition
    )
    type_readable = capacity_operating_system_type_readable()
    type_readable_plural = capacity_operating_system_type_readable_plural()


class MockCapacityPriceApiClient(MockApiClient):
    endpoint = "capacity_price"
    endpoint_definition_class = MockCapacityPriceUserSpecifiableOpenApiDefinition
    type_readable = capacity_price_type_readable()
    type_readable_plural = capacity_price_type_readable_plural()


class MockCapacityResourceQuotaApiClient(MockApiClient):
    endpoint = "capacity_resource_quota"
    endpoint_definition_class = (
        MockCapacityResourceQuotaUserSpecifiableOpenApiDefinition
    )
    type_readable = capacity_resource_quota_type_readable()
    type_readable_plural = capacity_resource_quota_type_readable_plural()


# Localities
class MockLocalityApiClient(MockApiClient):
    endpoint = "locality"
    endpoint_definition_class = MockLocalityUserSpecifiableOpenApiDefinition
    type_readable = locality_type_readable()
    type_readable_plural = locality_type_readable_plural()


# Column Metadata
class MockColumnMetadataApiClient(MockApiClient, BaseColumnMetadataApiClient):
    endpoint = "column_metadata"
    endpoint_definition_class = MockColumnMetadataUserSpecifiableOpenApiDefinition
    type_readable = "column metadata"
    type_readable_plural = "column metadata"

    def get_resources_by_category(self, category: str):
        resources = self.get_resources()
        return [r for r in resources if r.get("category") == category]

    def get_by_table_name(self, table_name: str):
        resources = self.get_resources()
        return [
            r
            for r in resources
            if (
                r.get("category") not in self.disabled_categories
                and r.get("table_name") == table_name
            )
        ]

    def get_resources_for_enabled_categories(self):
        resources = self._get_resources()
        return [
            r for r in resources if r.get("category") not in self.disabled_categories
        ]

    def get_resources_for_disabled_categories(self):
        resources = self._get_resources()
        return [r for r in resources if r.get("category") in self.disabled_categories]


class MockCloudCapacityColumnMetadataApiClient(MockColumnMetadataApiClient):
    disabled_categories = ["Edge Specific", "Networking"]

    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [
            r
            for r in resources
            if (
                r.get("table_name") == "capacity"
                and r.get("category") not in self.disabled_categories
            )
        ]


class MockEdgeCapacityColumnMetadataApiClient(MockColumnMetadataApiClient):
    disabled_categories = ["System Specific"]

    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [
            r
            for r in resources
            if (
                r.get("table_name") == "capacity"
                and r.get("category") not in self.disabled_categories
            )
        ]


class MockApplicationColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [r for r in resources if (r.get("table_name") == "application")]


class MockApplicationMicroserviceColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [
            r for r in resources if (r.get("table_name") == "application_microservice")
        ]
