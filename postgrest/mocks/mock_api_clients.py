from django.conf import settings

from editor.api.mocks.mock_base_api_clients import (
    BaseColumnMetadataApiClient,
    MockApiClient,
)
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
    endpoint_definition_class = ApplicationBehaviourUserSpecifiableOpenApiDefinition


class ApplicationColocateApiClient(MockApiClient):
    endpoint_definition_class = ApplicationColocateUserSpecifiableOpenApiDefinition


class ApplicationEnvironmentVarApiClient(MockApiClient):
    endpoint_definition_class = (
        ApplicationEnvironmentVarUserSpecifiableOpenApiDefinition
    )


class ApplicationPrefResourceProviderApiClient(MockApiClient):
    endpoint_definition_class = (
        ApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition
    )


class ApplicationSecurityRuleApiClient(MockApiClient):
    endpoint_definition_class = ApplicationSecurityRuleUserSpecifiableOpenApiDefinition


class ApplicationVolumeApiClient(MockApiClient):
    endpoint_definition_class = ApplicationVolumeUserSpecifiableOpenApiDefinition


# Capacities
class CloudCapacityApiClient(MockApiClient):
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition


class EdgeCapacityApiClient(MockApiClient):
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition


class CapacityEnergyConsumptionApiClient(MockApiClient):
    endpoint_definition_class = (
        CapacityEnergyConsumptionUserSpecifiableOpenApiDefinition
    )


class CapacityInstanceTypeApiClient(MockApiClient):
    endpoint_definition_class = CapacityInstanceTypeUserSpecifiableOpenApiDefinition


class CapacityOperatingSystemApiClient(MockApiClient):
    endpoint_definition_class = CapacityOperatingSystemUserSpecifiableOpenApiDefinition


class CapacityPriceApiClient(MockApiClient):
    endpoint_definition_class = CapacityPriceUserSpecifiableOpenApiDefinition


class CapacityResourceQuotaApiClient(MockApiClient):
    endpoint_definition_class = CapacityResourceQuotaUserSpecifiableOpenApiDefinition


# Localities
class LocalityApiClient(MockApiClient):
    endpoint_definition_class = LocalityUserSpecifiableOpenApiDefinition


# Column Metadata
class MockColumnMetadataApiClient(MockApiClient, BaseColumnMetadataApiClient):
    """This class is intended to be subclassed and shouldn't be
    instantiated directly.
    """

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
