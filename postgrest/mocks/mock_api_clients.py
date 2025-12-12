import os

from django.conf import settings

from postgrest.base.base_api_clients import BaseColumnMetadataApiClient
from postgrest.mocks.base.mock_base_api_clients import MockApiClient
from postgrest.mocks.mock_definitions import (
    MockColumnMetadataUserSpecifiableOpenApiDefinition,
)

from .mock_definitions import (
    ApplicationBehaviourUserSpecifiableOpenApiDefinition,
    ApplicationColocateUserSpecifiableOpenApiDefinition,
    ApplicationEnvironmentVarUserSpecifiableOpenApiDefinition,
    ApplicationMicroserviceUserSpecifiableOpenApiDefinition,
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
    LocalityUserSpecifiableOpenApiDefinition,
)

BASE_DIR = settings.BASE_DIR


# Applications
class ApplicationApiClient(MockApiClient):
    endpoint = "application"
    endpoint_definition_class = ApplicationUserSpecifiableOpenApiDefinition


class ApplicationMicroserviceApiClient(MockApiClient):
    endpoint = "application_microservice"
    endpoint_definition_class = ApplicationMicroserviceUserSpecifiableOpenApiDefinition


class ApplicationBehaviourApiClient(MockApiClient):
    endpoint = "application_behaviour"
    endpoint_definition_class = ApplicationBehaviourUserSpecifiableOpenApiDefinition


class ApplicationColocateApiClient(MockApiClient):
    endpoint = "application_colocate"
    endpoint_definition_class = ApplicationColocateUserSpecifiableOpenApiDefinition


class ApplicationEnvironmentVarApiClient(MockApiClient):
    endpoint = "application_environment_var"
    endpoint_definition_class = (
        ApplicationEnvironmentVarUserSpecifiableOpenApiDefinition
    )


class ApplicationPrefResourceProviderApiClient(MockApiClient):
    endpoint = "application_pref_resource_provider"
    endpoint_definition_class = (
        ApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition
    )


class ApplicationSecurityRuleApiClient(MockApiClient):
    endpoint = "application_security_rule"
    endpoint_definition_class = ApplicationSecurityRuleUserSpecifiableOpenApiDefinition


class ApplicationVolumeApiClient(MockApiClient):
    endpoint = "application_volume"
    endpoint_definition_class = ApplicationVolumeUserSpecifiableOpenApiDefinition


# Capacities
class CloudCapacityApiClient(MockApiClient):
    endpoint = "capacity"
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition

    @property
    def path_to_data(self):
        return os.path.join(self.path_to_data_dir, "cloud_capacity.json")

    @property
    def path_to_temp_data(self):
        return os.path.join(self.path_to_temp_data_dir, "cloud_capacity.json")


class EdgeCapacityApiClient(MockApiClient):
    endpoint = "capacity"
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition

    @property
    def path_to_data(self):
        return os.path.join(self.path_to_data_dir, "edge_capacity.json")

    @property
    def path_to_temp_data(self):
        return os.path.join(self.path_to_temp_data_dir, "edge_capacity.json")


class CapacityEnergyConsumptionApiClient(MockApiClient):
    endpoint = "capacity_energy_consumption"
    endpoint_definition_class = (
        CapacityEnergyConsumptionUserSpecifiableOpenApiDefinition
    )


class CapacityInstanceTypeApiClient(MockApiClient):
    endpoint = "capacity_instance_type"
    endpoint_definition_class = CapacityInstanceTypeUserSpecifiableOpenApiDefinition


class CapacityOperatingSystemApiClient(MockApiClient):
    endpoint = "capacity_operating_system"
    endpoint_definition_class = CapacityOperatingSystemUserSpecifiableOpenApiDefinition


class CapacityPriceApiClient(MockApiClient):
    endpoint = "capacity_price"
    endpoint_definition_class = CapacityPriceUserSpecifiableOpenApiDefinition


class CapacityResourceQuotaApiClient(MockApiClient):
    endpoint = "capacity_resource_quota"
    endpoint_definition_class = CapacityResourceQuotaUserSpecifiableOpenApiDefinition


# Localities
class LocalityApiClient(MockApiClient):
    endpoint = "locality"
    endpoint_definition_class = LocalityUserSpecifiableOpenApiDefinition


# Column Metadata
class MockColumnMetadataApiClient(MockApiClient, BaseColumnMetadataApiClient):
    endpoint = "column_metadata"
    endpoint_definition_class = MockColumnMetadataUserSpecifiableOpenApiDefinition

    def get_resources_by_category(self, category: str):
        resources = self.get_resources()
        return [
            r
            for r in resources
            if (
                r.get("category") not in self.disabled_categories
                and r.get("category") == category
            )
        ]

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

    def get_resources_for_disabled_categories(self):
        resources = self._get_resources()
        return [r for r in resources if r.get("category") in self.disabled_categories]


class CloudCapacityColumnMetadataApiClient(MockColumnMetadataApiClient):
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


class EdgeCapacityColumnMetadataApiClient(MockColumnMetadataApiClient):
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
