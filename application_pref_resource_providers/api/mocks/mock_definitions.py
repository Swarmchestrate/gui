import os

from django.conf import settings

from application_pref_resource_providers.api.definitions import (
    ApplicationPrefResourceProviderUserSpecifiableOpenApiDefinitionMixin,
)
from editor.api.mocks.mock_base_definitions import MockUserSpecifiableOpenApiDefinition


class ApplicationPrefResourceProviderUserSpecifiableOpenApiDefinition(
    ApplicationPrefResourceProviderUserSpecifiableOpenApiDefinitionMixin,
    MockUserSpecifiableOpenApiDefinition,
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "application_pref_resource_providers",
        "api",
        "mocks",
        "jsons",
        "definitions",
        "application_pref_resource_provider.json",
    )
