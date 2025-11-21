from editor.api.base_definitions import UserSpecifiableOpenApiDefinitionMixin


class LocalityUserSpecifiableOpenApiDefinitionMixin(
    UserSpecifiableOpenApiDefinitionMixin
):
    id_field = "locality_id"
