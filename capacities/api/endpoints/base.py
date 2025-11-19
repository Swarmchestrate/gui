from capacities.api.definitions import CapacityUserSpecifiableOpenApiDefinition
from editor.api.endpoints.base import ApiEndpoint


class BaseCapacityApiEndpoint(ApiEndpoint):
    def __init__(self) -> None:
        self.endpoint = "capacity"
        super().__init__()


class CapacityApiEndpoint(BaseCapacityApiEndpoint):
    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition
