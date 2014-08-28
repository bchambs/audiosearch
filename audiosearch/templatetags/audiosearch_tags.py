from django import template

register = template.Library()

@register.filter
def space_to_plus(url):
    try:
        return url.replace(' ', '+')
    except AttributeError:
        return ''


@register.filter
def build_query_string(q_params):
    if q_params:
        return '&'.join("%s=%s" % (key,value) for (key,value) in q_params.iteritems())
    else:
        return ''
