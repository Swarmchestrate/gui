import os

from django.conf import settings

from capacity_energy_consumptions.api.definitions import (
    CapacityEnergyConsumptionUserSpecifiableOpenApiDefinitionMixin,
)
from editor.api.mocks.mock_base_definitions import MockUserSpecifiableOpenApiDefinition


class CapacityEnergyConsumptionUserSpecifiableOpenApiDefinition(
    CapacityEnergyConsumptionUserSpecifiableOpenApiDefinitionMixin,
    MockUserSpecifiableOpenApiDefinition,
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "capacity_energy_consumptions",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "capacity_energy_consumption.json",
    )
