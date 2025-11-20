from capacities.api.definitions import CapacityUserSpecifiableOpenApiDefinition
from editor.api.endpoints.base import ApiEndpoint


class CapacityApiEndpoint(ApiEndpoint):
    def __init__(self) -> None:
        self.endpoint = "capacity"
        super().__init__()

    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition
