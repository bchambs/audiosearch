from django import template

register = template.Library()

@register.filter
def space_to_plus(url):
    try:
        return url.replace(' ', '+')
    except AttributeError:
        return ''


@register.filter
def to_percent(float):
    p = round(float * 100)
    percent = str(p).split('.')

    if len(percent) > 0:
        return percent[0] + " %"
    else:
        return ''
