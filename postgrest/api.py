import logging

from .api_configs.base_config import (
    BaseResource,
    BaseDefinition,
    BaseOpenApiSpecification
)
from .api_configs.config_finder import (
    BaseApiClient,
    BaseEndpoint,
)



logger = logging.getLogger(__name__)


class Resource(BaseResource):
    pass


class Definition(BaseDefinition):
    pass


class Endpoint(BaseEndpoint):
    pass


class OpenApiSpecification(BaseOpenApiSpecification):
    pass


class ApiClient(BaseApiClient):
    pass