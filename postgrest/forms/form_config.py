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


class PropertiesMetadata:
    def __init__(
            self,
            definition_name: str,
            openapi_spec: dict,
            column_metadata: list[dict]):
        self._definition_name = definition_name
        definitions = openapi_spec.get("definitions")
        self._definition = definitions.get(definition_name)
        self._column_metadata_as_dict = self._create_dict_copy_of_column_metadata(
            column_metadata
        )
    
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
    
    def as_dict(self) -> dict:
        """Generates a dict of PropertyMetadata instances mapped
        by property name.

        Returns:
            dict: a dict of PropertyMetadata instances mapped by
            property name.
        """
        properties_metadata_as_dict = {}
        properties_from_definition = self._definition.get("properties")
        names_of_required_properties = self._definition.get("required")
        for name, metadata in properties_from_definition.items():
            is_required = name in names_of_required_properties
            column_metadata_for_table = self._column_metadata_as_dict.get(
                self._definition_name
            )
            column_metadata_for_property = column_metadata_for_table.get(name, {})
            properties_metadata_as_dict.update({
                name: PropertyMetadata(
                    name=name,
                    is_required=is_required,
                    format=metadata.get("format"),
                    type=metadata.get("type"),
                    description=metadata.get("description"),
                    enum=metadata.get("enum"),
                    title=column_metadata_for_property.get("title"),
                    category=column_metadata_for_property.get("category"),
                    help_text=column_metadata_for_property.get("description")
                )
            })
        return properties_metadata_as_dict


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
    _properties_metadata: dict[str, PropertyMetadata]
    
    def __init__(self, properties_metadata: dict[str, PropertyMetadata]):
        self._properties_metadata = properties_metadata
        
    def _get_field_config_class_from_format(self, format: str):
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
        for name, metadata in self._properties_metadata.items():
            field_config_class = self._get_field_config_class_from_format(metadata.format)
            if metadata.enum:
                choices = [
                    (field_enum, field_enum.replace("_", " "))
                    for field_enum in metadata.enum
                ]
                choices.insert(0, ("", "None"))
                field_config_class = ChoiceFieldConfig(choices)
            fields.update({
                name: field_config_class(
                    name,
                    metadata.is_required,
                    metadata.title,
                    metadata.help_text,
                    metadata.category,
                ).get_field()
            })
        return fields
