from editor.api.base_api_clients import ApiEndpoint, ColumnMetadataApiEndpoint
from instance_types.api.definitions import InstanceTypeUserSpecifiableOpenApiDefinition


class InstanceTypeApiEndpoint(ApiEndpoint):
    endpoint_definition_class = InstanceTypeUserSpecifiableOpenApiDefinition

    def __init__(self) -> None:
        self.endpoint = "instance_types"
        super().__init__()

    def _prepare_update_data(self, data: dict):
        data = super()._prepare_update_data(data)
        data.pop("updated_at", None)
        data.pop(self.endpoint_definition.id_field, None)
        return data


class InstanceTypeColumnMetadataApiEndpoint(ColumnMetadataApiEndpoint):
    def get_registrations(self, params: dict | None = None) -> list[dict]:
        if not params:
            params = dict()
        params.update(
            {
                "table_name": "eq.instance_types",
            }
        )
        return super().get_registrations(params=params)
