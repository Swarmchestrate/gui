from django import template

from instance_types.utils import (
    instance_type_type_readable,
    instance_type_type_readable_plural,
)

register = template.Library()


register.simple_tag(instance_type_type_readable)
register.simple_tag(instance_type_type_readable_plural)
