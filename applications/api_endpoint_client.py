from .definitions import ApplicationUserSpecifiableOpenApiDefinition

from editor.api_endpoint_client import ApiEndpointClient, ColumnMetadataApiEndpointClient


class ApplicationApiEndpointClient(ApiEndpointClient):
    endpoint_definition_class = ApplicationUserSpecifiableOpenApiDefinition

    def __init__(self) -> None:
        self.endpoint = 'application'
        super().__init__()


class ApplicationColumnMetadataApiEndpointClient(ColumnMetadataApiEndpointClient):
    def get_registrations(self, params: dict = None):
        if not params:
            params = dict()
        params.update({
            'table_name': 'eq.application',
        })
        return super().get_registrations(params=params)
