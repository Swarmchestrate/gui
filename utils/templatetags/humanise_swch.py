from django import template

from ..humanise import (
    humanise_resource_type,
    humanise_resource_type_plural,
    resource_label,
)


register = template.Library()


register.filter("humanise_resource_type", humanise_resource_type)
register.filter("humanise_resource_type_plural", humanise_resource_type_plural)


@register.simple_tag
def label_for(resource, resource_type, resource_id):
    """Name a row, falling back to its type and id when it has no name."""
    return resource_label(resource, resource_type, resource_id)
