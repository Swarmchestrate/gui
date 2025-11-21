from editor.api.definitions.base import UserSpecifiableOpenApiDefinitionMixin


class LocalityUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "locality_id"
