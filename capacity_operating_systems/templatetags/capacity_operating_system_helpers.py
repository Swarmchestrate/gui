from django import template

from capacity_operating_systems.utils import (
    capacity_operating_system_type_readable,
    capacity_operating_system_type_readable_plural,
)

register = template.Library()


register.simple_tag(capacity_operating_system_type_readable)
register.simple_tag(capacity_operating_system_type_readable_plural)
