from django import template

from capacity_energy_consumptions.utils import (
    capacity_energy_consumption_type_readable,
    capacity_energy_consumption_type_readable_plural,
)

register = template.Library()


register.simple_tag(capacity_energy_consumption_type_readable)
register.simple_tag(capacity_energy_consumption_type_readable_plural)
