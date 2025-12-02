from django import template

from capacity_prices.utils import (
    capacity_price_type_readable,
    capacity_price_type_readable_plural,
)

register = template.Library()


register.simple_tag(capacity_price_type_readable)
register.simple_tag(capacity_price_type_readable_plural)
