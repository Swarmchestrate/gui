from editor.api.endpoints.base import ColumnMetadataApiEndpoint

from .base import BaseEdgeCapacityColumnMetadataApiEndpoint, CapacityApiEndpoint


class EdgeCapacityApiEndpoint(CapacityApiEndpoint):
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update({"resource_type": "eq.Edge"})
        return super().get_registrations(params)

    def register(self, data: dict):
        data.update({"resource_type": "Edge"})
        return super().register(data)

    def delete(self, registration_id: int, params: dict | None = None):
        if not params:
            params = dict()
        params.update({"resource_type": "eq.Edge"})
        return super().delete(registration_id, params)


class EdgeCapacityColumnMetadataApiEndpoint(
    BaseEdgeCapacityColumnMetadataApiEndpoint, ColumnMetadataApiEndpoint
):
    disabled_categories = ["System Specific"]

    def get_registrations(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.capacity",
            }
        )
        return super().get_registrations(params)

    def get_registrations_by_category(self, category: str):
        return self.get_registrations(params={"category": f'eq."{category}"'})
