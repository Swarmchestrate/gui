from django import template

from application_colocations.utils import (
    application_colocation_type_readable,
    application_colocation_type_readable_plural,
)

register = template.Library()


register.simple_tag(application_colocation_type_readable)
register.simple_tag(application_colocation_type_readable_plural)
