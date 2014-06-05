from django import template

register = template.Library()

# f = expected float object
#
# take float f and convert to percentage
def to_percent(f):
    if type(f) == float:
        temp = round (f * 100)
        return int(temp)
    else:
        return '???'		# should throw an exception 

register.filter('to_percent',to_percent)
