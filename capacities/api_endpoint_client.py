from .definitions import CapacityUserSpecifiableOpenApiDefinition

from editor.api_endpoint_client import ApiEndpointClient, ColumnMetadataApiEndpointClient


class BaseCapacityApiEndpointClient(ApiEndpointClient):
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition

    def __init__(self) -> None:
        self.endpoint = 'capacity'
        super().__init__()


class CapacityApiEndpointClient(BaseCapacityApiEndpointClient):
    pass


class CloudCapacityApiEndpointClient(BaseCapacityApiEndpointClient):
    def get_registrations(self, params: dict = dict()):
        params.update({'resource_type': 'eq.Cloud'})
        return super().get_registrations(params=params)

    def register(self, data: dict):
        data.update({'resource_type': 'Cloud'})
        return super().register(data)

    def delete(self, registration_id: int, params: dict = dict()):
        params.update({'resource_type': 'eq.Cloud'})
        return super().delete(registration_id, params)


class CloudCapacityColumnMetadataApiEndpointClient(ColumnMetadataApiEndpointClient):
    def get_registrations(self, params: dict = dict()):
        params.update({
            'table_name': 'eq.capacity',
            'category': 'neq.Edge Specific',
        })
        return super().get_registrations(params)


class EdgeCapacityApiEndpointClient(BaseCapacityApiEndpointClient):
    def get_registrations(self, params: dict = dict()):
        params.update({'resource_type': 'eq.Edge'})
        return super().get_registrations(params)

    def register(self, data: dict):
        data.update({'resource_type': 'Edge'})
        return super().register(data)

    def delete(self, registration_id: int, params: dict = dict()):
        params.update({'resource_type': 'eq.Edge'})
        return super().delete(registration_id, params)


class EdgeCapacityColumnMetadataApiEndpointClient(ColumnMetadataApiEndpointClient):
    def get_registrations(self, params: dict = dict()):
        params.update({
            'table_name': 'eq.capacity',
            'category': 'neq.System Specific',
        })
        return super().get_registrations(params)
