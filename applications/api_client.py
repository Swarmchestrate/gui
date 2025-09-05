from .definitions import ApplicationUserSpecifiableOpenApiDefinition

from editor.api_client import ApiClient


class ApplicationApiClient(ApiClient):
    endpoint_definition_class = ApplicationUserSpecifiableOpenApiDefinition

    def __init__(self) -> None:
        self.endpoint = 'application'
        super().__init__()