from dataclasses import dataclass, field


@dataclass
class PropertyMetadata:
    """Combines metadata about a property initially
    described in a PostgREST OpenAPI 2.0 specification
    (in definitions -> <definition_name> -> properties)
    with additional metadata from the column_metadata table.
    """
    # Custom attributes to make it easier to work
    # with FieldConfig.
    name: str
    is_pk: bool = False
    is_required: bool = False
    refers_to_table_name: str | None = None
    created_from_table_name: str | None = None
    has_fk_relation_to_secondary_table: str | None = None
    # Defined in the PostgREST OpenAPI Specification
    format: str | None = None
    type: str | None = None
    description: str | None = None # used by PostgREST to denote if a foreign key.
    enum: list | None = field(default_factory=list) # only set by if enum field.
    # Value/label pairs offered instead of free text, for a column whose valid
    # values are known somewhere other than the database - the TOSCA profile's
    # capability properties, for one. Takes precedence over enum, because it
    # carries a readable label rather than just the stored value.
    choices: list | None = None
    # Defined in the corresponding column metadata
    # record (if it exists).
    title: str | None = None
    category: str | None = None
    help_text: str | None = None
