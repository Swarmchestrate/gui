from django import template

register = template.Library()


@register.filter
def get_key_value_or_blank_string(d: dict, key: str):
    try:
        return d.get(key, '')
    except AttributeError:
        return ''