from django import template

register = template.Library()

#take float f and conver to percentage
def to_percent(f):
    temp = round (f * 100)
    return int(temp)

register.filter('to_percent',to_percent)