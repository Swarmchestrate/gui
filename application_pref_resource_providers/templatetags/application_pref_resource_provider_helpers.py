from django import template

from application_pref_resource_providers.utils import (
    application_pref_resource_provider_type_readable,
    application_pref_resource_provider_type_readable_plural,
)

register = template.Library()


register.simple_tag(application_pref_resource_provider_type_readable)
register.simple_tag(application_pref_resource_provider_type_readable_plural)
