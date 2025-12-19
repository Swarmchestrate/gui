import casefy
from dateutil import parser
from django import template

register = template.Library()


@register.filter
def split_by_colon(value: str):
    return value.split(":")


@register.filter
def kebab_case(value: str):
    return casefy.kebabcase(value)


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


# Credit: https://stackoverflow.com/a/32801096
@register.filter
def next(list_, current_index):
    """Returns the next element of the list using the current index
    if it exists. Otherwise returns an empty string.
    """
    try:
        return list_[int(current_index) + 1]  # access the next element
    except Exception:
        return ""  # return empty string in case of exception


@register.filter
def previous(list_, current_index):
    """Returns the previous element of the list using the current index
    if it exists. Otherwise returns an empty string.
    """
    try:
        return list_[int(current_index) - 1]  # access the next element
    except Exception:
        return ""  # return empty string in case of exception
