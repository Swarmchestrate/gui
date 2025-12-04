from editor.api.base_definitions import (
    UserSpecifiableOpenApiDefinition,
    UserSpecifiableOpenApiDefinitionMixin,
)


class ApplicationBehaviourUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "behaviour_id"
    definition_name = "application_behaviour"


class ApplicationBehaviourUserSpecifiableOpenApiDefinition(
    ApplicationBehaviourUserSpecifiableOpenApiDefinitionMixin,
    UserSpecifiableOpenApiDefinition,
):
    pass
