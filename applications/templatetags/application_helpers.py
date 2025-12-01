from django import template

from applications.utils import (
    application_type_readable,
    application_type_readable_plural,
)

register = template.Library()


register.simple_tag(application_type_readable)
register.simple_tag(application_type_readable_plural)
