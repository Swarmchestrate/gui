from django import template

from ..humanise import (
    humanise_resource_type,
    humanise_resource_type_plural,
)


register = template.Library()


register.filter("humanise_resource_type", humanise_resource_type)
register.filter("humanise_resource_type_plural", humanise_resource_type_plural)