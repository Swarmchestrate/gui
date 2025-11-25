from abc import ABC

from editor.api.base_api_clients import (
    BaseColumnMetadataApiClient,
    ColumnMetadataApiClient,
)

from .capacity_api_clients import CapacityApiClient


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


class BaseEdgeCapacityColumnMetadataApiClient(BaseColumnMetadataApiClient, ABC):
    disabled_categories = ["System Specific"]


class EdgeCapacityColumnMetadataApiClient(
    BaseEdgeCapacityColumnMetadataApiClient, ColumnMetadataApiClient
):
    disabled_categories = ["System Specific"]

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
