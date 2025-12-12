import json
import os

from django.conf import settings

from postgrest.base.base_definitions import (
    BaseOpenApiDefinition,
    UserSpecifiableOpenApiDefinitionMixin,
)


class MockOpenApiDefinition(BaseOpenApiDefinition):
    """This class is intended to be subclassed and shouldn't be
    instantiated directly.
    """

    path_to_definitions_dir = os.path.join(
        settings.BASE_DIR, "postgrest", "mocks", "jsons", "definitions"
    )

    def _get_definition(self) -> dict:
        definition = None
        path_to_definition = os.path.join(
            self.path_to_definitions_dir,
            f"{self.definition_name}.json",
        )
        with open(
            path_to_definition,
            "r",
        ) as f:
            definition = json.loads(f.read())
        return definition


class MockUserSpecifiableOpenApiDefinition(
    MockOpenApiDefinition, UserSpecifiableOpenApiDefinitionMixin
):
    def _get_all_definitions(self) -> dict:
        definitions = dict()
        for definition_class in MockUserSpecifiableOpenApiDefinition.__subclasses__():
            if definition_class.definition_name == self.definition_name:
                continue
            definition = definition_class()
            definitions.update(
                {definition.definition_name: definition._get_definition()}
            )
        return definitions
