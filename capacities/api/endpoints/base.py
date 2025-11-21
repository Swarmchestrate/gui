from abc import ABC

from capacities.api.definitions.user_specifiable_definitions import (
    CapacityUserSpecifiableOpenApiDefinition,
)
from editor.api.endpoints.base import ApiEndpoint, BaseColumnMetadataApiEndpoint


class CapacityApiEndpoint(ApiEndpoint):
    def __init__(self) -> None:
        self.endpoint = "capacity"
        super().__init__()

    endpoint_definition_class = CapacityUserSpecifiableOpenApiDefinition


class BaseCloudCapacityColumnMetadataApiEndpoint(BaseColumnMetadataApiEndpoint, ABC):
    disabled_categories = ["Edge Specific", "Networking"]


class BaseEdgeCapacityColumnMetadataApiEndpoint(BaseColumnMetadataApiEndpoint, ABC):
    disabled_categories = ["System Specific"]
