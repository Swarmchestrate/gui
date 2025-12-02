from django import template

from capacity_resource_quotas.utils import (
    capacity_resource_quota_type_readable,
    capacity_resource_quota_type_readable_plural,
)

register = template.Library()


register.simple_tag(capacity_resource_quota_type_readable)
register.simple_tag(capacity_resource_quota_type_readable_plural)
