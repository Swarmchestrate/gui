from abc import ABC

from capacities.api.definitions import (
    CapacityUserSpecifiableOpenApiDefinition,
)
from editor.api.base_api_clients import ApiEndpoint, BaseColumnMetadataApiEndpoint


class CapacityApiEndpoint(ApiEndpoint):
    def __init__(self) -> None:
        self.endpoint = "capacity"
        super().__init__()

    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition


class BaseCloudCapacityColumnMetadataApiEndpoint(BaseColumnMetadataApiEndpoint, ABC):
    disabled_categories = ["Edge Specific", "Networking"]


class BaseEdgeCapacityColumnMetadataApiEndpoint(BaseColumnMetadataApiEndpoint, ABC):
    disabled_categories = ["System Specific"]
