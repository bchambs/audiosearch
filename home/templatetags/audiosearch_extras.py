from django import template

register = template.Library()

#take float f and conver to percentage
def to_percent(f):
    if type(f) == float:
        temp = round (f * 100)
        return int(temp)
    else:
        return '???'

register.filter('to_percent',to_percent)