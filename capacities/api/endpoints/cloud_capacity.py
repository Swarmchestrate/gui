from editor.api.endpoints.base import ColumnMetadataApiEndpoint

from .base import BaseCapacityApiEndpoint


class CloudCapacityApiEndpoint(BaseCapacityApiEndpoint):
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update({"resource_type": "eq.Cloud"})
        return super().get_registrations(params=params)

    def register(self, data: dict):
        data.update({"resource_type": "Cloud"})
        return super().register(data)

    def delete(self, registration_id: int, params: dict | None = None):
        if not params:
            params = dict()
        params.update({"resource_type": "eq.Cloud"})
        return super().delete(registration_id, params)


class CloudCapacityColumnMetadataApiEndpoint(ColumnMetadataApiEndpoint):
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.capacity",
            }
        )
        if "category" not in params:
            params.update(
                {
                    "category": "neq.Edge Specific",
                }
            )
            return super().get_registrations(params)
        params.update(
            {
                "and": f"(category.{params.get('category')},category.neq.Edge Specific)",
            }
        )
        params.pop("category", None)
        return super().get_registrations(params)

    def get_by_category(self, category: str):
        return self.get_registrations(params={"category": f'eq."{category}"'})
