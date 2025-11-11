from django import template
from django.urls import reverse

register = template.Library()


@register.inclusion_tag('breadcrumbs/item.html')
def breadcrumb_item(text, viewname, *args, **kwargs):
    return {
        'text': text,
        'url': reverse(viewname, args=[*args, *kwargs.values()])
    }

@register.inclusion_tag('breadcrumbs/item_active.html')
def breadcrumb_item_active(text):
    return {
        'text': text
    }
