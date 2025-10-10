from .definitions import InstanceTypeUserSpecifiableOpenApiDefinition

from editor.api_endpoint_client import ApiEndpointClient, ColumnMetadataApiEndpointClient


class InstanceTypeApiEndpointClient(ApiEndpointClient):
    endpoint_definition_class = InstanceTypeUserSpecifiableOpenApiDefinition

    def __init__(self) -> None:
        self.endpoint = 'instance_types'
        super().__init__()


class InstanceTypeColumnMetadataApiEndpointClient(ColumnMetadataApiEndpointClient):
    def get_registrations(self, params: dict = None):
        if not params:
            params = dict()
        params.update({
            'table_name': 'eq.instance_types',
        })
        return super().get_registrations(params=params)
