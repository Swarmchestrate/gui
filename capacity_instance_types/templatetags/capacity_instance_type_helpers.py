from django import template

from capacity_instance_types.utils import (
    capacity_instance_type_type_readable,
    capacity_instance_type_type_readable_plural,
)

register = template.Library()


register.simple_tag(capacity_instance_type_type_readable)
register.simple_tag(capacity_instance_type_type_readable_plural)
