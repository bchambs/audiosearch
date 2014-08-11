from django import template

register = template.Library()

@register.filter
def space_to_plus(url):
    try:
        return url.replace(' ', '+')
    except AttributeError:
        return ''

