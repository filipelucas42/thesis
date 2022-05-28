from django import template

register = template.Library()

@register.filter(is_safe=True)
def method(value):
    return "<input type='hidden' name='__method' value='{}'>".format(value.lower())

@register.filter
def dict_item(dictionary, key):
    return dictionary.get(key)
