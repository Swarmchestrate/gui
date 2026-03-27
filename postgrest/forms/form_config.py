from django import forms
from enum import Enum

from .property_metadata import PropertyMetadata
from .field_config import (
    BooleanFieldConfig,
    ChoiceFieldConfig,
    DateFieldConfig,
    DefaultFieldConfig,
    GeometryPointFieldConfig,
    IntegerFieldConfig,
    JsonFieldConfig,
    NumericFieldConfig,
)


class Properties:
    def __init__(
            self,
            definition_name: str,
            openapi_spec: dict,
            column_metadata: list[dict],
            column_metadata_table_name: str | None = None):
        definitions = openapi_spec.get("definitions")
        self._definition = definitions.get(definition_name, {})
        self._one_to_many_properties = dict()
        self._column_metadata_as_dict = self._create_dict_copy_of_column_metadata(
            column_metadata
        )
        self._column_metadata_table_name = definition_name
        if not column_metadata_table_name:
            return
        self._column_metadata_table_name = column_metadata_table_name
    
    def _create_dict_copy_of_column_metadata(
            self,
            column_metadata: list[dict]) -> dict:
        """Maps a list of records from the column metadata
        table to a dict, grouping metadata in the following order:
        table_name -> column_name -> column_metadata.

        Args:
            column_metadata (list[dict]): a list of column_metadata records.
        Returns:
            dict: a list of column metadata mapped to a dict.
        """
        column_metadata_as_dict = {}
        for cm_record in column_metadata:
            table_name = cm_record.get("table_name")
            column_name = cm_record.get("column_name")
            if table_name not in column_metadata_as_dict:
                column_metadata_as_dict.update({
                    table_name: {},
                })
            column_metadata_as_dict[table_name].update({
                column_name: {},
            })
            column_metadata_as_dict[table_name][column_name].update(
                cm_record
            )
        return column_metadata_as_dict

    def _get_property_metadata_instance(
            self,
            name: str,
            metadata: dict,
            extra_metadata_for_property: dict,
            is_required: bool):
        return PropertyMetadata(
            name=name,
            is_required=is_required,
            format=metadata.get("format"),
            type=metadata.get("type"),
            description=metadata.get("description"),
            enum=metadata.get("enum"),
            title=extra_metadata_for_property.get("title"),
            category=extra_metadata_for_property.get("category"),
            help_text=extra_metadata_for_property.get("description")
        )

    def add_one_to_many_property(self, name: str):
        self._one_to_many_properties.update({
            name: dict(),
        })

    def as_categorised_dict(self) -> dict:
        UNKNOWN_CATEGORY = 'Uncategorised'
        categorised_properties_as_dict = {UNKNOWN_CATEGORY: dict()}
        properties_from_definition = self._definition.get("properties", dict())
        properties_from_definition.update(self._one_to_many_properties)
        names_of_required_properties = self._definition.get("required", list())
        column_metadata_for_table = self._column_metadata_as_dict.get(
            self._column_metadata_table_name,
            {}
        )
        for name, metadata in properties_from_definition.items():
            is_required = name in names_of_required_properties
            extra_metadata_for_property = column_metadata_for_table.get(name, {})
            property_category = extra_metadata_for_property.get("category")
            if not property_category:
                categorised_properties_as_dict[UNKNOWN_CATEGORY].update({
                    name: self._get_property_metadata_instance(
                        name,
                        metadata,
                        extra_metadata_for_property,
                        is_required
                    )
                })
                continue
            if property_category not in categorised_properties_as_dict:
                categorised_properties_as_dict.update({
                    property_category: dict(),
                })
            categorised_properties_as_dict[property_category].update({
                name: self._get_property_metadata_instance(
                    name,
                    metadata,
                    extra_metadata_for_property,
                    is_required
                )
            })
        return categorised_properties_as_dict
    
    def as_dict(self) -> dict:
        """Generates a dict of PropertyMetadata instances mapped
        by property name.

        Returns:
            dict: a dict of PropertyMetadata instances mapped by
            property name.
        """
        properties_as_dict = {}
        properties_from_definition = self._definition.get("properties", dict())
        properties_from_definition.update(self._one_to_many_properties)
        names_of_required_properties = self._definition.get("required", list())
        column_metadata_for_table = self._column_metadata_as_dict.get(
            self._column_metadata_table_name,
            {}
        )
        for name, metadata in properties_from_definition.items():
            is_required = name in names_of_required_properties
            extra_metadata_for_property = column_metadata_for_table.get(name, {})
            properties_as_dict.update({
                name: self._get_property_metadata_instance(
                    name,
                    metadata,
                    extra_metadata_for_property,
                    is_required
                )
            })
        return properties_as_dict


class OasDefinitionPropertyFormat(Enum):
    BOOLEAN = "boolean"
    CHARACTER_VARYING = "character varying"
    DATE = "timestamp without time zone"
    DOUBLE_PRECISION = "double precision"
    GEOMETRY = "public.geometry"
    INTEGER = "integer"
    JSONB = "jsonb"
    NUMERIC = "numeric"
    TEXT = "text"
    TEXT_ARRAY = "text[]"


class FormConfig:
    initial = None
    _properties: dict[str, PropertyMetadata]
    
    def __init__(self, properties: dict[str, PropertyMetadata]):
        self._properties = properties
        
    def _get_field_config_class_from_format(self, format: str):
        format_enum = None
        try:
            format_enum = OasDefinitionPropertyFormat(format)
        except ValueError:
            pass

        match format_enum:
            case OasDefinitionPropertyFormat.BOOLEAN:
                return BooleanFieldConfig
            case OasDefinitionPropertyFormat.DATE:
                return DateFieldConfig
            case OasDefinitionPropertyFormat.GEOMETRY:
                return GeometryPointFieldConfig
            case OasDefinitionPropertyFormat.INTEGER:
                return IntegerFieldConfig
            case OasDefinitionPropertyFormat.NUMERIC | OasDefinitionPropertyFormat.DOUBLE_PRECISION:
                return NumericFieldConfig
            case OasDefinitionPropertyFormat.TEXT_ARRAY | OasDefinitionPropertyFormat.JSONB:
                return JsonFieldConfig
        return DefaultFieldConfig

    def get_fields(self) -> dict:
        fields = dict()
        for name, metadata in self._properties.items():
            field_config_class = self._get_field_config_class_from_format(metadata.format)
            additional_args = []
            if metadata.enum:
                choices = [
                    (field_enum, field_enum.replace("_", " "))
                    for field_enum in metadata.enum
                ]
                choices.insert(0, ("", "None"))
                additional_args.append(choices)
                field_config_class = ChoiceFieldConfig
            fields.update({
                name: field_config_class(
                    *additional_args,
                    name,
                    metadata.is_required,
                    metadata.title,
                    metadata.help_text,
                    metadata.category,
                ).get_field()
            })
        return fields
