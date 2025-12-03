from django import template

from application_volumes.utils import (
    application_volume_type_readable,
    application_volume_type_readable_plural,
)

register = template.Library()


register.simple_tag(application_volume_type_readable)
register.simple_tag(application_volume_type_readable_plural)
