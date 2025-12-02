from editor.api.base_definitions import (
    UserSpecifiableOpenApiDefinition,
    UserSpecifiableOpenApiDefinitionMixin,
)


class ApplicationBehaviourUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "behaviour_id"


class InstanceTypeUserSpecifiableOpenApiDefinition(
    ApplicationBehaviourUserSpecifiableOpenApiDefinitionMixin,
    UserSpecifiableOpenApiDefinition,
):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "application_behaviour"


class ApplicationBehaviourUserSpecifiableOpenApiDefinition(
    ApplicationBehaviourUserSpecifiableOpenApiDefinitionMixin,
    UserSpecifiableOpenApiDefinition,
):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "application_behaviour"
