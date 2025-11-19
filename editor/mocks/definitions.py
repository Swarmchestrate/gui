import json
import os

from django.conf import settings

from editor.api.abc import BaseOpenApiDefinition
from editor.api.definition_mixins import UserSpecifiableOpenApiDefinitionMixin


class MockOpenApiDefinition(BaseOpenApiDefinition):
    """This class is intended to be subclassed and shouldn't be
    instantiated directly.
    """

    path_to_definition: os.PathLike | str

    def _get_definition(self) -> dict:
        definition = None
        with open(self.path_to_definition, "r") as f:
            definition = json.loads(f.read())
        return definition


class MockUserSpecifiableOpenApiDefinition(
    MockOpenApiDefinition, UserSpecifiableOpenApiDefinitionMixin
):
    pass


class MockColumnMetadataUserSpecifiableOpenApiDefinition(
    MockUserSpecifiableOpenApiDefinition
):
    path_to_definition = os.path.join(
        settings.BASE_DIR,
        "editor",
        "mocks",
        "jsons",
        "definitions",
        "column_metadata.json",
    )
