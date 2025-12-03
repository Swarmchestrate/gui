from django import template

from application_security_rules.utils import (
    application_security_rule_type_readable,
    application_security_rule_type_readable_plural,
)

register = template.Library()


register.simple_tag(application_security_rule_type_readable)
register.simple_tag(application_security_rule_type_readable_plural)
