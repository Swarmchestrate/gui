from abc import ABC

from editor.api.abc import BaseColumnMetadataApiEndpoint


class BaseCloudCapacityColumnMetadataApiEndpoint(BaseColumnMetadataApiEndpoint, ABC):
    disabled_categories = ["Edge Specific", "Networking"]


class BaseEdgeCapacityColumnMetadataApiEndpoint(BaseColumnMetadataApiEndpoint, ABC):
    disabled_categories = ["System Specific"]
