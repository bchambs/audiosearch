import ast

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


@register.filter
def print_context(wall_of_text):
    """
    Filter template context from Django's 'debug' template tag.
    Usage:
        {% filter print_context %} {% debug %} {% endfilter %}
    """

    generator = lambda text: iter(text.splitlines())
    lines = generator(wall_of_text)

    for line in lines:
        if 'user' in line:  # TODO: Context can span multiple lines
            print 
            try:
                token = line.split('}{').pop(2)
                context_string = "{" + token + "}"
                context = ast.literal_eval(context_string)
            except (IndexError, SyntaxError):
                print '{}Error parsing template context'.format(' ' * 4)
            else:
                print '{}Template Context'.format(' ' * 4)
                for k, v in context.iteritems():
                    print '{}{}: {}'.format('\t', k, v)
            finally:
                print
                return ''


