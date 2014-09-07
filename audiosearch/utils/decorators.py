from __future__ import absolute_import
from functools import wraps


def debug_view(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print 
        print '%s ->' % (f.__name__)
        print 
        
        view_result = f(*args, **kwargs)

        print 
        print '<-'
        print 
        return view_result
    return wrapper






# def my_decorator(f):
# ...     @wraps(f)
# ...     def wrapper(*args, **kwds):
# ...         print 'Calling decorated function'
# ...         return f(*args, **kwds)
# ...     return wrapper
