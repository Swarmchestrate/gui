"""Choices for columns whose valid values live outside the database.

Most dropdowns come from a Postgres enum, which PostgREST reports and the form
config turns into a select on its own. A few columns are different: a resource
requirement's target names a capability property of the TOSCA profile, so the
database has no way to know what is valid and stores plain text.

A provider registered here supplies those values, keyed by table and column, so
the editor stays generic and the knowledge stays with whichever app owns it.
"""
import logging
from typing import Callable, List, Tuple

logger = logging.getLogger(__name__)

Choices = List[Tuple[str, str]]

_providers: dict[tuple[str, str], Callable[[], Choices]] = {}


def register_field_choices(
        table_name: str,
        column_name: str,
        provider: Callable[[], Choices]) -> None:
    """Say where one column's choices come from."""
    _providers[(str(table_name), column_name)] = provider


def choices_for(table_name: str, column_name: str) -> Choices | None:
    """The choices for a column, or None when it is ordinary free text.

    A provider that fails is treated as having none, so a form still renders
    when whatever supplies the values is unreachable.
    """
    provider = _providers.get((str(table_name), column_name))
    if not provider:
        return None
    try:
        return provider() or None
    except Exception:
        logger.exception(
            "Could not load choices for %s.%s; leaving it as free text",
            table_name, column_name,
        )
        return None
