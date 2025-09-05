from .definitions import ApplicationUserSpecifiableOpenApiDefinition

from editor.api_endpoint_client import ApiEndpointClient


class ApplicationApiEndpointClient(ApiEndpointClient):
    endpoint_definition_class = ApplicationUserSpecifiableOpenApiDefinition

    def __init__(self) -> None:
        self.endpoint = 'application'
        super().__init__()