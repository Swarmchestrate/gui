import os

from django.conf import settings

from capacity_prices.api.definitions import (
    CapacityPriceUserSpecifiableOpenApiDefinitionMixin,
)
from editor.api.mocks.mock_base_definitions import MockUserSpecifiableOpenApiDefinition


class CapacityPriceUserSpecifiableOpenApiDefinition(
    CapacityPriceUserSpecifiableOpenApiDefinitionMixin,
    MockUserSpecifiableOpenApiDefinition,
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "capacity_prices",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "capacity_price.json",
    )
