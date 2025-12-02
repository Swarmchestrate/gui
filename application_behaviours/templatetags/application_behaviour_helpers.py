from django import template

from application_behaviours.utils import (
    application_behaviour_type_readable,
    application_behaviour_type_readable_plural,
)

register = template.Library()


register.simple_tag(application_behaviour_type_readable)
register.simple_tag(application_behaviour_type_readable_plural)
