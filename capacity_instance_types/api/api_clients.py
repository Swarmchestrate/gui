from capacity_instance_types.api.definitions import (
    CapacityInstanceTypeUserSpecifiableOpenApiDefinition,
)
from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
    ColumnMetadataApiClient,
)


class BaseCapacityInstanceTypeApiClient(BaseApiClient):
    endpoint = "capacity_instance_types"

    def _prepare_update_data(self, data: dict):
        data = super()._prepare_update_data(data)
        data.pop("updated_at", None)
        data.pop(self.endpoint_definition.id_field, None)
        return data


class CapacityInstanceTypeApiClient(BaseCapacityInstanceTypeApiClient, ApiClient):
    endpoint_definition_class = CapacityInstanceTypeUserSpecifiableOpenApiDefinition


class CapacityInstanceTypeColumnMetadataApiClient(ColumnMetadataApiClient):
    def get_resources(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.capacity_instance_types",
            }
        )
        return super().get_resources(params=params)
