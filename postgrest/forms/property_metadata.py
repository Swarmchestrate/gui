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
    is_required: bool = False
    # Defined in the PostgREST OpenAPI Specification
    format: str | None = None
    type: str | None = None
    description: str | None = None # used by PostgREST to denote if a foreign key.
    enum: list | None = field(default_factory=list) # only set by if enum field.
    # Defined in the corresponding column metadata
    # record (if it exists).
    title: str | None = None
    category: str | None = None
    help_text: str | None = None
