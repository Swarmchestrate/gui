from dateutil import parser
from django import template

register = template.Library()


@register.filter
def split_by_colon(value: str):
    return value.split(":")


@register.filter
def get_key_value_or_blank_string(d: dict, key: str):
    try:
        return d.get(key, "")
    except AttributeError:
        return ""


@register.filter
def get_key_value_or_empty_dict(d: dict, key: str):
    try:
        return d.get(key, dict())
    except AttributeError:
        return dict()


@register.filter
def convert_str_date(value: str):
    return parser.parse(value)
