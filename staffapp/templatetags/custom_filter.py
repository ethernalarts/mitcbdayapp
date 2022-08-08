
from django import template

register = template.Library()

@register.filter
def ifinlist(value, list):
    return value in list
