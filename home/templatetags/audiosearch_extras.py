from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# f = expected float object
#
# take float f and convert to percentage
def to_percent(f):

    if type(f) == float:
        temp = round (f * 100)
        return int(temp)
    else:
        return ''

register.filter('to_percent',to_percent)


# s = string
#
# surround the string with quotes and mark the object as 'javascript safe'.  this prevents JS from 
# translating quotes to '&quot' when django context objects are passed to JS functions.
def qsurround(s):

    return mark_safe("\"" + s + "\"")

register.filter('qsurround',qsurround)
