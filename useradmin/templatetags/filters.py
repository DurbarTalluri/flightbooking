from django import template
register= template.Library()

@register.filter
def element(dictionary, key):
    return dictionary[key]
register.filter('element',element)