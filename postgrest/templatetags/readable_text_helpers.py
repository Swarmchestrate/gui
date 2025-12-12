from django import template

from postgrest.readable_text_utils import (
    application_behaviour_type_readable,
    application_behaviour_type_readable_plural,
    application_colocation_type_readable,
    application_colocation_type_readable_plural,
    application_environment_var_type_readable,
    application_environment_var_type_readable_plural,
    application_pref_resource_provider_type_readable,
    application_pref_resource_provider_type_readable_plural,
    application_security_rule_type_readable,
    application_security_rule_type_readable_plural,
    application_type_readable,
    application_type_readable_plural,
    application_volume_type_readable,
    application_volume_type_readable_plural,
    capacity_energy_consumption_type_readable,
    capacity_energy_consumption_type_readable_plural,
    capacity_instance_type_type_readable,
    capacity_instance_type_type_readable_plural,
    capacity_operating_system_type_readable,
    capacity_operating_system_type_readable_plural,
    capacity_price_type_readable,
    capacity_price_type_readable_plural,
    capacity_resource_quota_type_readable,
    capacity_resource_quota_type_readable_plural,
    capacity_type_readable,
    capacity_type_readable_plural,
    cloud_capacity_type_readable,
    cloud_capacity_type_readable_plural,
    edge_capacity_type_readable,
    edge_capacity_type_readable_plural,
    locality_type_readable,
    locality_type_readable_plural,
)

register = template.Library()


register.simple_tag(application_behaviour_type_readable)
register.simple_tag(application_behaviour_type_readable_plural)
register.simple_tag(application_colocation_type_readable)
register.simple_tag(application_colocation_type_readable_plural)
register.simple_tag(application_environment_var_type_readable)
register.simple_tag(application_environment_var_type_readable_plural)
register.simple_tag(application_pref_resource_provider_type_readable)
register.simple_tag(application_pref_resource_provider_type_readable_plural)
register.simple_tag(application_security_rule_type_readable)
register.simple_tag(application_security_rule_type_readable_plural)
register.simple_tag(application_type_readable)
register.simple_tag(application_type_readable_plural)
register.simple_tag(application_volume_type_readable)
register.simple_tag(application_volume_type_readable_plural)
register.simple_tag(capacity_energy_consumption_type_readable)
register.simple_tag(capacity_energy_consumption_type_readable_plural)
register.simple_tag(capacity_instance_type_type_readable)
register.simple_tag(capacity_instance_type_type_readable_plural)
register.simple_tag(capacity_operating_system_type_readable)
register.simple_tag(capacity_operating_system_type_readable_plural)
register.simple_tag(capacity_price_type_readable)
register.simple_tag(capacity_price_type_readable_plural)
register.simple_tag(capacity_resource_quota_type_readable)
register.simple_tag(capacity_resource_quota_type_readable_plural)
register.simple_tag(capacity_type_readable)
register.simple_tag(capacity_type_readable_plural)
register.simple_tag(cloud_capacity_type_readable)
register.simple_tag(cloud_capacity_type_readable_plural)
register.simple_tag(edge_capacity_type_readable)
register.simple_tag(edge_capacity_type_readable_plural)
register.simple_tag(locality_type_readable)
register.simple_tag(locality_type_readable_plural)
