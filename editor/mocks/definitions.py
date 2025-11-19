import json
import os

from django.conf import settings

from editor.mixins.definition_mixins import UserSpecifiableOpenApiDefinitionMixin

from ..abc import BaseOpenApiDefinition


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
        "definitions",
        "column_metadata.json",
    )
