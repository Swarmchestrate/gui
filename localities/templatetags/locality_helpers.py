from django import template

from localities.utils import (
    locality_type_readable,
    locality_type_readable_plural,
)

register = template.Library()


register.simple_tag(locality_type_readable)
register.simple_tag(locality_type_readable_plural)
