"""Widgets for columns whose database type does not say how to edit them.

A jsonb column may hold arbitrary JSON or a flat name/value map, and a text
column may hold a label or a sixty-line MiniZinc rule. The type alone cannot tell
these apart, so the app that knows registers the widget here, keyed by table and
column, and the editor stays generic.
"""

KEY_VALUE = "key_value"
TEXTAREA = "textarea"

_widgets: dict[tuple[str, str], str] = {}


def register_field_widget(table_name: str, column_name: str, widget: str) -> None:
    """Say how one column should be edited."""
    _widgets[(str(table_name), column_name)] = widget


def widget_for(table_name: str, column_name: str) -> str | None:
    """The widget registered for a column, or None to go by its type."""
    return _widgets.get((str(table_name), column_name))
