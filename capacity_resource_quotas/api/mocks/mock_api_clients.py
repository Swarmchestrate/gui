import os

from django.conf import settings

from capacity_resource_quotas.api.api_clients import (
    BaseCapacityResourceQuotaApiClient,
)
from capacity_resource_quotas.api.mocks.mock_definitions import (
    CapacityResourceQuotaUserSpecifiableOpenApiDefinition,
)
from editor.api.mocks.mock_base_api_clients import (
    MockApiClient,
    MockColumnMetadataApiClient,
)

BASE_DIR = settings.BASE_DIR


class CapacityResourceQuotaApiClient(BaseCapacityResourceQuotaApiClient, MockApiClient):
    endpoint_definition_class = CapacityResourceQuotaUserSpecifiableOpenApiDefinition
    path_to_data = os.path.join(
        BASE_DIR,
        "capacity_resource_quotas",
        "api",
        "mocks",
        "jsons",
        "data",
        "capacity_resource_quotas.json",
    )
    path_to_temp_data_dir = os.path.join(BASE_DIR, "capacity_resource_quotas", "temp")


class CapacityResourceQuotaColumnMetadataApiClient(MockColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        resources = super().get_resources()
        return [
            r for r in resources if r.get("table_name") == "capacity_resource_quota"
        ]
