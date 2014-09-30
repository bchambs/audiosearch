from __future__ import absolute_import

from django import template

from audiosearch.conf.display import ROWS_PER_TABLE as INTERVAL


register = template.Library()


# @register.simple_tag(takes_context=True)
# def set_page(qparams, offset):
#     page_num = page + offset
#     return "?page={}".format(page_num)
#     # page_num = page_nav + offset
#     # qs = '&'.join("%s=%s" % (k, v) for (k, v) in params.iteritems())
#     # return ''.join(['?', qs])


@register.filter
def build_query(params):
    """Create query string."""
    if not params:
        return ''
    qs = '&'.join("%s=%s" % (k, v) for (k, v) in params.iteritems())
    return ''.join(['?', qs])


@register.filter
def offset(page):
    """Calculate page index offset."""
    return 1 if page < 2 else (page * INTERVAL) + 1


@register.filter
def divideby(results, rows_per_table):
    """Divide and truncate decimal."""
    return results / rows_per_table


@register.filter
def inspect(item):
    print '\nin filter'
    print '\t{}'.format(type(item))
    print '\t{}'.format(len(item))
    print '\t{}'.format(item)
    print 'out filter\n'
    return item


########################
########################
########################


@register.filter
def space_to_plus(url):
    # TODO use builtin iri_to_uri
    try:
        return url.replace(' ', '+')
    except AttributeError:
        return ''

