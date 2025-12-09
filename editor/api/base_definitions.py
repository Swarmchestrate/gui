from abc import abstractmethod

import lxml.html


class BaseOpenApiDefinition:
    id_field: str
    definition_name: str

    # Properties
    @property
    def description(self) -> str:
        return self._get_definition().get("description", "")

    # Public methods
    def get_field(self, field_name: str) -> dict:
        return self._get_definition().get("properties", {}).get(field_name, {})

    # Non-public methods
    @abstractmethod
    def _get_all_definitions(self) -> dict:
        pass

    @abstractmethod
    def _get_definition(self) -> dict:
        pass

    def _get_required_field_names(self):
        return self._get_definition().get("required", list())

    def _get_all_fields(self) -> dict:
        properties = self._get_definition().get("properties", {})
        return properties

    def _get_foreign_key_fields(self) -> dict:
        properties = self._get_definition().get("properties", {})
        foreign_key_properties = dict()
        for property_name, property_metadata in properties.items():
            description = property_metadata.get("description", "")
            if not description:
                continue
            fk_table_names = lxml.html.fromstring(description).xpath("fk/@table")
            if not fk_table_names:
                continue
            property_metadata.update(
                {
                    "table_name": next(iter(fk_table_names)),
                }
            )
            foreign_key_properties.update({property_name: property_metadata})
        return foreign_key_properties

    def _get_one_to_one_fields(self) -> dict:
        foreign_key_fields = self._get_foreign_key_fields()
        one_to_one_properties = dict()
        for property_name, property_metadata in foreign_key_fields.items():
            is_unique = property_metadata.get("unique", False)
            if not is_unique:
                continue
            one_to_one_properties.update({property_name: property_metadata})
        return one_to_one_properties


class OpenApiDefinition(BaseOpenApiDefinition):
    openapi_spec: dict

    def __init__(self, openapi_spec: dict) -> None:
        self.openapi_spec = openapi_spec

    def _get_all_definitions(self) -> dict:
        return self.openapi_spec.get("definitions", {})

    def _get_definition(self) -> dict:
        return self.openapi_spec.get("definitions", {}).get(self.definition_name, {})


class UserSpecifiableOpenApiDefinitionMixin(BaseOpenApiDefinition):
    # Non-public methods
    def _get_auto_generated_field_names(self) -> list:
        return list(
            [
                self.id_field,
                "created_at",
                "updated_at",
            ]
        )

    def _get_disabled_field_names(self) -> list:
        return list()

    def _get_non_user_specifiable_field_names(self) -> list:
        return list(
            set(
                self._get_auto_generated_field_names()
                + self._get_disabled_field_names()
            )
        )

    def _get_all_user_specifiable_fields(self, include_one_to_many_fields: bool = True):
        all_fields = self._get_all_fields()
        if include_one_to_many_fields:
            all_fields = self._add_one_to_many_properties(all_fields)
        return {
            key: value
            for key, value in all_fields.items()
            if key not in self._get_non_user_specifiable_field_names()
        }

    def _get_required_user_specifiable_field_names(self):
        required_field_names = set(self._get_required_field_names())
        auto_generated_field_names = set(self._get_non_user_specifiable_field_names())
        return list(required_field_names - auto_generated_field_names)

    def _add_one_to_many_properties(self, base_properties: dict) -> dict:
        definitions = self._get_all_definitions()
        for definition_key, definition in definitions.items():
            properties = definition.get("properties", dict())
            if not properties:
                continue
            properties_containing_endpoint_name = [
                property
                for property in properties.values()
                if (
                    self.definition_name in property.get("description", "")
                    and lxml.html.fromstring(property.get("description", "")).xpath(
                        "fk/@table"
                    )
                )
            ]
            if not properties_containing_endpoint_name:
                continue
            if definition_key in base_properties:
                continue
            base_properties.update(
                {
                    definition_key: {
                        "type": "one_to_many",
                        "endpoint": definition_key,
                    }
                }
            )
        return base_properties

    def _get_one_to_many_fields(self) -> dict:
        foreign_key_fields = self._get_foreign_key_fields()
        one_to_many_properties = dict()
        for property_name, property_metadata in foreign_key_fields.items():
            is_unique = property_metadata.get("unique", False)
            if is_unique:
                continue
            one_to_many_properties.update({property_name: property_metadata})
        return one_to_many_properties

    # Public methods
    def get_all_user_specifiable_fields(self, include_one_to_many_fields: bool = True):
        return self._get_all_user_specifiable_fields(
            include_one_to_many_fields=include_one_to_many_fields
        )

    def get_user_specifiable_foreign_key_fields(self):
        return self._get_foreign_key_fields()

    def get_user_specifiable_one_to_one_fields(self):
        return self._get_one_to_one_fields()

    def get_user_specifiable_one_to_many_fields(self):
        return self._get_one_to_many_fields()

    def get_required_field_names(self):
        return self._get_required_field_names()


class UserSpecifiableOpenApiDefinition(
    OpenApiDefinition, UserSpecifiableOpenApiDefinitionMixin
):
    pass


class ColumnMetadataUserSpecifiableOpenApiDefinition(UserSpecifiableOpenApiDefinition):
    def __init__(self, openapi_spec: dict) -> None:
        super().__init__(openapi_spec)
        self.definition_name = "column_metadata"
        self.id_field = ""
