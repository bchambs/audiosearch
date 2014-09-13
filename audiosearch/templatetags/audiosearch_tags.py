from django import template

register = template.Library()

@register.filter
def space_to_plus(url):
    # TODO use builtin
    try:
        return url.replace(' ', '+')
    except AttributeError:
        return ''


@register.filter
def to_query_string(params):
    try:
        qs = '&'.join("%s=%s" % (k, v) for (k, v) in params.iteritems())
    except AttributeError:
        qs = ''
    return qs

@register.filter
def inspect(item):
    print '\nin filter'
    print '\t{}'.format(type(item))
    print '\t{}'.format(len(item))
    print '\t{}'.format(item)
    print 'out filter\n'

    return item
