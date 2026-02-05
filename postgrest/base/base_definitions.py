from abc import abstractmethod

import lxml.html


# The PostgREST API uses OAS ver. 2 for the its
# OAS.
# "Definition" refers to a data structure stored in
# the global "definitions" section described in OAS
# ver. 2:
# https://swagger.io/docs/specification/v2_0/basic-structure/#input-and-output-models.
class BaseOpenApiDefinition:
    definition_name: str
    _pk_field_name: str

    # Properties
    @property
    def pk_field_name(self) -> str | None:
        if hasattr(self, "_pk_field_name"):
            return self._pk_field_name
        for field_name, field_metadata in self._get_all_fields().items():
            description = field_metadata.get("description")
            if not description:
                continue
            is_pk = lxml.html.fromstring(description).xpath("pk")
            if not is_pk:
                continue
            self._pk_field_name = field_name
            return field_name
        return None

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
                    "fk_table_name": next(iter(fk_table_names), None),
                }
            )
            foreign_key_properties.update({property_name: property_metadata})
        return foreign_key_properties

    def _get_one_to_one_fields(self) -> dict:
        return self._get_foreign_key_fields()

    def _get_many_to_one_fields(self) -> dict:
        return self._get_foreign_key_fields()

    def _get_one_to_many_fields(self) -> dict:
        one_to_many_properties = dict()
        definitions = self._get_all_definitions()
        for definition_key, definition in definitions.items():
            properties = definition.get("properties", dict())
            if not properties:
                continue
            for property in properties.values():
                description = property.get("description", "")
                if not description:
                    continue
                if self.definition_name not in description:
                    continue
                fk_table_name = next(
                    iter(lxml.html.fromstring(description).xpath("fk/@table")), None
                )
                fk_column_name = next(
                    iter(lxml.html.fromstring(description).xpath("fk/@column")), None
                )
                if not fk_table_name or not fk_column_name:
                    continue
                one_to_many_properties.update(
                    {
                        definition_key: {
                            "type": "one_to_many",
                            "fk_table_name": definition_key,
                            "fk_table_column_name": fk_column_name,
                        }
                    }
                )
        return one_to_many_properties


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
                self.pk_field_name,
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
        one_to_many_properties = self._get_one_to_many_fields()
        base_properties.update(one_to_many_properties)
        return base_properties

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

    def get_user_specifiable_many_to_one_fields(self):
        return self._get_many_to_one_fields()

    def get_required_field_names(self):
        return self._get_required_field_names()


class UserSpecifiableOpenApiDefinition(
    OpenApiDefinition, UserSpecifiableOpenApiDefinitionMixin
):
    pass
