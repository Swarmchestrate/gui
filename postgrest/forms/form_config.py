import lxml.html
from collections.abc import Callable
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

from postgrest.api import Definition, Resource
from utils.constants import UNKNOWN_ATTRIBUTE_CATEGORY
from utils.humanise import humanise_resource_type_plural


class ColumnMetadata:
    def __init__(self, data: list[Resource]):
        self._data = data

    def as_dict(self):
        """Maps a list of records from the column metadata
        table to a dict, grouping metadata in the following order:
        table_name -> column_name -> column_metadata.

        Args:
            column_metadata (list[dict]): a list of column_metadata records.
        Returns:
            dict: a list of column metadata mapped to a dict.
        """
        column_metadata_as_dict = {}
        for resource in self._data:
            resource_as_dict = resource.as_dict()
            table_name = resource_as_dict.get("table_name")
            column_name = resource_as_dict.get("column_name")
            if table_name not in column_metadata_as_dict:
                column_metadata_as_dict.update({
                    table_name: {},
                })
            column_metadata_as_dict[table_name].update({
                column_name: {},
            })
            column_metadata_as_dict[table_name][column_name].update(
                resource_as_dict
            )
        return column_metadata_as_dict


class Properties:
    def __init__(
            self,
            definition_name: str,
            definition: Definition,
            column_metadata: ColumnMetadata,
            column_metadata_table_name: str | None = None):
        self._definition = definition
        self._column_metadata_as_dict = column_metadata.as_dict()
        self._column_metadata_table_name = definition_name
        if not column_metadata_table_name:
            return
        self._column_metadata_table_name = column_metadata_table_name
    
    def _get_foreign_key_table_name(self, description: str):
        if not description:
            return None
        return next(iter(
            lxml.html.fromstring(description).xpath("fk/@table")
        ), None)

    def _get_property_metadata_instance(
            self,
            name: str,
            metadata: dict,
            extra_metadata_for_property: dict,
            is_required: bool):
        return PropertyMetadata(
            name=name,
            is_pk=(name == self._definition.pk_column_name),
            is_required=is_required,
            refers_to_table_name=self._get_foreign_key_table_name(metadata.get("description")),
            format=metadata.get("format"),
            type=metadata.get("type"),
            description=metadata.get("description"),
            enum=metadata.get("enum"),
            title=extra_metadata_for_property.get("title"),
            category=extra_metadata_for_property.get("category"),
            help_text=extra_metadata_for_property.get("description")
        )
    
    def as_dict(self) -> dict[str, PropertyMetadata]:
        """Generates a dict of PropertyMetadata instances mapped
        by property name.

        Returns:
            dict: a dict of PropertyMetadata instances mapped by
            property name.
        """
        properties_as_dict = {}
        properties_from_definition = self._definition.properties
        names_of_required_properties = self._definition.required
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
    
    
class OneToManyProperties:
    def __init__(
            self,
            table_name: str,
            fk_table_names: list[str],
            column_metadata: ColumnMetadata,
            column_metadata_table_name: str = None):
        self._table_name = table_name
        self._fk_table_names = fk_table_names
        self._column_metadata_as_dict = column_metadata.as_dict()
        self._column_metadata_table_name = column_metadata_table_name
        if not column_metadata_table_name:
            self._column_metadata_table_name = table_name

    def as_dict(self):
        """Generates a dict of PropertyMetadata instances mapped
        by table name.

        Returns:
            dict: a dict of PropertyMetadata instances mapped by
            table name.
        """
        properties_as_dict = {}
        column_metadata_for_table = self._column_metadata_as_dict.get(
            self._column_metadata_table_name,
            {}
        )
        for table_name in self._fk_table_names:
            extra_metadata_for_property = column_metadata_for_table.get(table_name, {})
            properties_as_dict.update({
                table_name: PropertyMetadata(
                    name=table_name,
                    is_pk=False,
                    created_from_table_name=table_name,
                    is_required=False,
                    format=None,
                    type=None,
                    description=None,
                    enum=None,
                    title=extra_metadata_for_property.get("title") or humanise_resource_type_plural(table_name).title(),
                    category=extra_metadata_for_property.get("category"),
                    help_text=extra_metadata_for_property.get("description")
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
    extra_disabled_properties: list[str]
    initial = None
    _properties: dict[str, PropertyMetadata]
    _default_disabled_properties = [
        "created_at",
        "updated_at",
    ]
    
    def __init__(
            self,
            properties: dict[str, PropertyMetadata],
            one_to_many_properties: dict[str, PropertyMetadata] = None,
            extra_disabled_properties: list[str] = None):
        self._properties = properties
        if one_to_many_properties:
            self._properties.update(one_to_many_properties)
        self.extra_disabled_properties = extra_disabled_properties
        if not extra_disabled_properties:
            self.extra_disabled_properties = list()
        
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
    
    def _get_field_config_instance(self, name: str, metadata: PropertyMetadata):
        field_config_class = self._get_field_config_class_from_format(metadata.format)
        additional_args = []
        if metadata.enum:
            choices = [
                (field_enum, field_enum.replace("_", " "))
                for field_enum in metadata.enum
            ]
            # Fields with choices are optional, so
            # a blank choice is added so an actual
            # choice isn't set by default.
            choices.insert(0, ("", "None"))
            additional_args.append(choices)
            field_config_class = ChoiceFieldConfig
        return field_config_class(
            *additional_args,
            name,
            metadata,
            metadata.is_required,
            metadata.title,
            metadata.help_text,
            metadata.category,
        )

    def get_properties(self):
        properties = dict()
        for name, metadata in self._properties.items():
            if (metadata.is_pk
                or name in self._default_disabled_properties
                or name in self.extra_disabled_properties):
                continue
            properties.update({
                name: metadata,
            })
        return properties

    def _get_fields(
            self,
            extra_skip_conditions: list[Callable[[PropertyMetadata], bool]] = None) -> dict:
        fields = dict()
        for name, metadata in self._properties.items():
            if (metadata.is_pk
                or name in self._default_disabled_properties
                or name in self.extra_disabled_properties):
                continue
            if extra_skip_conditions and any(
                check(metadata)
                for check in extra_skip_conditions
            ):
                continue
            field_config_instance = self._get_field_config_instance(name, metadata)
            fields.update({
                name: field_config_instance.get_field(),
            })
        return fields

    def get_fields(self) -> dict:
        return self._get_fields()
    
    def get_fields_for_category(self, category) -> dict:
        return self._get_fields(extra_skip_conditions=[
            lambda metadata: not category and metadata.category,
            lambda metadata: category and not metadata.category,
            lambda metadata: not (category == metadata.category),
        ])
    
    def get_required_fields(self) -> dict:
        return self._get_fields(extra_skip_conditions=[
            lambda metadata: not metadata.is_required,
        ])

    def get_field_categories(self) -> list[str]:
        categories = list()
        for fieldname, field in self._get_fields().items():
            if field.category in categories:
                continue
            if field.category == UNKNOWN_ATTRIBUTE_CATEGORY:
                categories.append(None)
                continue
            categories.append(field.category)
        return categories