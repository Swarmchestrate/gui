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
    TextArrayFieldConfig,
)

from postgrest.api import (
    Definition,
    OpenApiSpecification,
    Resource
)
from postgrest.table_names import TableNames
from utils.constants import UNKNOWN_ATTRIBUTE_CATEGORY
from utils.humanise import humanise_enum_value, humanise_resource_type_plural


MAIN_TABLE_NAMES = [
    TableNames.APPLICATION,
    TableNames.APPLICATION_MICROSERVICE,
    TableNames.APPLICATION_NEW,
    TableNames.CAPACITY,
    TableNames.CAPACITY_NEW,
]


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
            openapi_spec: OpenApiSpecification,
            column_metadata: ColumnMetadata,
            column_metadata_table_name: str | None = None):
        self._openapi_spec = openapi_spec
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

    def _is_primary_key(self, description: str):
        if not description:
            return None
        pk_element = next(iter(
            lxml.html.fromstring(description).xpath("pk")
        ), None)
        if pk_element is not None:
            return True
        return False

    def _get_property_metadata_instance(
            self,
            name: str,
            metadata: dict,
            column_metadata_for_property: dict,
            is_required: bool):
        refers_to_table_name = self._get_foreign_key_table_name(metadata.get("description"))
        has_fk_relation_to_secondary_table = False
        if refers_to_table_name:
            table_name = self._definition.get_foreign_key_table_name_for_column(
                name
            )
            definition = self._openapi_spec.get_definition(table_name)
            references_to_other_tables = definition.find_references_to_other_tables()
            is_fk_ref_made_to_secondary_table = any(
                (other_table_name not in MAIN_TABLE_NAMES
                and not (other_table_name == table_name))
                for other_table_name in references_to_other_tables
            )
            is_fk_ref_made_from_secondary_table = self._openapi_spec.find_references_to_table(
                table_name
            )
            has_fk_relation_to_secondary_table = is_fk_ref_made_to_secondary_table or is_fk_ref_made_from_secondary_table
        return PropertyMetadata(
            name=name,
            is_pk=self._is_primary_key(metadata.get("description")),
            is_required=is_required,
            refers_to_table_name=refers_to_table_name,
            has_fk_relation_to_secondary_table=has_fk_relation_to_secondary_table,
            format=metadata.get("format"),
            type=metadata.get("type"),
            description=metadata.get("description"),
            enum=metadata.get("enum"),
            title=column_metadata_for_property.get("title"),
            category=column_metadata_for_property.get("category"),
            help_text=column_metadata_for_property.get("description")
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
            column_metadata_for_property = column_metadata_for_table.get(name, {})
            properties_as_dict.update({
                name: self._get_property_metadata_instance(
                    name,
                    metadata,
                    column_metadata_for_property,
                    is_required
                )
            })
        return properties_as_dict
    
    
class OneToManyProperties:
    def __init__(
            self,
            table_name: str,
            definitions_by_table_name: dict[str, Definition],
            openapi_spec: OpenApiSpecification,
            column_metadata: ColumnMetadata,
            column_metadata_table_name: str = None):
        self._table_name = table_name
        self._definitions_by_table_name = definitions_by_table_name
        self._openapi_spec = openapi_spec
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
        for table_name, definition in self._definitions_by_table_name.items():
            column_metadata_for_property = column_metadata_for_table.get(table_name, {})
            references_to_other_tables = definition.find_references_to_other_tables()
            has_fk_relation_to_secondary_table = False
            is_fk_ref_made_to_secondary_table = any(
                (other_table_name not in MAIN_TABLE_NAMES
                and not (other_table_name == table_name))
                for other_table_name in references_to_other_tables
            )
            is_fk_ref_made_from_secondary_table = self._openapi_spec.find_references_to_table(
                table_name
            )
            has_fk_relation_to_secondary_table = is_fk_ref_made_to_secondary_table or is_fk_ref_made_from_secondary_table
            properties_as_dict.update({
                table_name: PropertyMetadata(
                    name=table_name,
                    is_pk=False,
                    created_from_table_name=table_name,
                    has_fk_relation_to_secondary_table=has_fk_relation_to_secondary_table,
                    is_required=False,
                    format=None,
                    type=None,
                    description=None,
                    enum=None,
                    title=column_metadata_for_property.get("title") or humanise_resource_type_plural(table_name).title(),
                    category=column_metadata_for_property.get("category"),
                    help_text=column_metadata_for_property.get("description")
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
    # Properties that can't be anticipated in advance -
    # see postgrest.views.XOneToManyRelationFormView for
    # examples.
    _additional_disabled_properties: list[str]
    _properties: dict[str, PropertyMetadata]
    PROPERTIES_SET_AT_SAVE_TIME = [
        "created_at",
        "updated_at",
    ]
    PROPERTIES_SET_THROUGH_URL = [
        TableNames.APPLICATION,
        TableNames.APPLICATION_NEW,
        TableNames.CAPACITY,
        TableNames.CAPACITY_NEW,
        f"{TableNames.APPLICATION}_id",
        f"{TableNames.CAPACITY}_id",
    ]
    
    def __init__(
            self,
            properties: dict[str, PropertyMetadata],
            one_to_many_properties: dict[str, PropertyMetadata] = None,
            additional_disabled_properties: list[str] = None):
        self._properties = properties
        if one_to_many_properties:
            self._properties.update(one_to_many_properties)
        if not additional_disabled_properties:
            additional_disabled_properties = list()
        self._additional_disabled_properties = additional_disabled_properties

    @property
    def disabled_properties(self):
        # Override this to sync disabled properties across
        # views (e.g., the wizard fields which are restricted
        # in the view that renders the wizard should match the
        # fields which are restricted when an update from that
        # wizard is received by another view).
        return [
            *self.PROPERTIES_SET_AT_SAVE_TIME,
            *self.PROPERTIES_SET_THROUGH_URL,
            *self._additional_disabled_properties,
        ]
        
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
            case OasDefinitionPropertyFormat.JSONB:
                return JsonFieldConfig
            case OasDefinitionPropertyFormat.TEXT_ARRAY:
                return TextArrayFieldConfig
        return DefaultFieldConfig
    
    def _get_field_config_instance(self, name: str, metadata: PropertyMetadata):
        field_config_class = self._get_field_config_class_from_format(metadata.format)
        additional_args = []
        if metadata.choices:
            choices = list(metadata.choices)
            if not metadata.is_required:
                choices.insert(0, ("", "None"))
            additional_args.append(choices)
            field_config_class = ChoiceFieldConfig
        elif metadata.enum:
            choices = [
                (field_enum, humanise_enum_value(field_enum))
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
                or name in self.disabled_properties):
                continue
            properties.update({
                name: metadata,
            })
        return properties

    def _get_fields(
            self,
            include_pk_fields: bool = False,
            extra_skip_conditions: list[Callable[[PropertyMetadata], bool]] = None) -> dict:
        fields = dict()
        for name, metadata in self._properties.items():
            if (metadata.is_pk and not include_pk_fields):
                continue
            if (name in self.disabled_properties):
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

    def get_fields(self, include_pk_fields: bool = False) -> dict:
        return self._get_fields(include_pk_fields=include_pk_fields)
    
    def get_fields_for_category(self, category) -> dict:
        return self._get_fields(extra_skip_conditions=[
            lambda metadata: not category and metadata.category,
            lambda metadata: category and not metadata.category,
            lambda metadata: category and not (category == metadata.category),
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