from editor.api.base_definitions import UserSpecifiableOpenApiDefinition


class ApplicationUserSpecifiableOpenApiDefinitionMixin:
    id_field = "application_id"
    definition_name = "application"


class ApplicationMicroserviceUserSpecifiableOpenApiDefinitionMixin:
    id_field = "id"
    definition_name = "application_microservice"


class ApplicationUserSpecifiableOpenApiDefinition(
    ApplicationUserSpecifiableOpenApiDefinitionMixin, UserSpecifiableOpenApiDefinition
):
    pass


class ApplicationMicroserviceUserSpecifiableOpenApiDefinition(
    ApplicationMicroserviceUserSpecifiableOpenApiDefinitionMixin,
    UserSpecifiableOpenApiDefinition,
):
    pass
