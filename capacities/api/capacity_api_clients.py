from editor.api.base_api_clients import (
    ApiEndpoint,
    BaseApiEndpoint,
)

from .definitions import (
    CapacityUserSpecifiableOpenApiDefinition,
)


class BaseCapacityApiEndpoint(BaseApiEndpoint):
    endpoint = "capacity"


class CapacityApiEndpoint(BaseCapacityApiEndpoint, ApiEndpoint):
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition
