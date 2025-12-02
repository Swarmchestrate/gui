import os

from django.conf import settings

from capacity_resource_quotas.api.definitions import (
    CapacityResourceQuotaUserSpecifiableOpenApiDefinitionMixin,
)
from editor.api.mocks.mock_base_definitions import MockUserSpecifiableOpenApiDefinition


class CapacityResourceQuotaUserSpecifiableOpenApiDefinition(
    CapacityResourceQuotaUserSpecifiableOpenApiDefinitionMixin,
    MockUserSpecifiableOpenApiDefinition,
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "capacity_resource_quotas",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "capacity_resource_quota.json",
    )
