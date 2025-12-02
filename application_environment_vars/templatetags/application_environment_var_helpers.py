from django import template

from application_environment_vars.utils import (
    application_environment_var_type_readable,
    application_environment_var_type_readable_plural,
)

register = template.Library()


register.simple_tag(application_environment_var_type_readable)
register.simple_tag(application_environment_var_type_readable_plural)
