from django import template

from capacities.utils import (
    capacity_type_readable,
    capacity_type_readable_plural,
    cloud_capacity_type_readable,
    cloud_capacity_type_readable_plural,
    edge_capacity_type_readable,
    edge_capacity_type_readable_plural,
)

register = template.Library()


register.simple_tag(capacity_type_readable)
register.simple_tag(capacity_type_readable_plural)
register.simple_tag(cloud_capacity_type_readable)
register.simple_tag(cloud_capacity_type_readable_plural)
register.simple_tag(edge_capacity_type_readable)
register.simple_tag(edge_capacity_type_readable_plural)
