from editor.api.base_api_clients import (
    ApiClient,
    BaseApiClient,
)

from .definitions import (
    CapacityUserSpecifiableOpenApiDefinition,
)


class BaseCapacityApiClient(BaseApiClient):
    endpoint = "capacity"


class CapacityApiClient(BaseCapacityApiClient, ApiClient):
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition
