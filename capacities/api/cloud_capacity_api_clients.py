from abc import ABC

from editor.api.base_api_clients import (
    BaseColumnMetadataApiClient,
    ColumnMetadataApiClient,
)

from .capacity_api_clients import (
    CapacityApiClient,
)


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


class BaseCloudCapacityColumnMetadataApiClient(BaseColumnMetadataApiClient, ABC):
    disabled_categories = ["Edge Specific", "Networking"]


class CloudCapacityColumnMetadataApiClient(
    BaseCloudCapacityColumnMetadataApiClient, ColumnMetadataApiClient
):
    disabled_categories = ["Edge Specific", "Networking"]

    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.capacity",
            }
        )
        return super().get_resources(params)

    def get_resources_by_category(self, category: str):
        return self.get_resources(params={"category": f'eq."{category}"'})
