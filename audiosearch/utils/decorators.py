from __future__ import absolute_import

from functools import wraps
    

def stdout_gap(view_func):
    """
    Visual cue for view debugging.  Seperates view function 'print's from the
    django test server HTTP response spam.
    """
    title = "\n{} . {} . {}".format('=' * 5, view_func.__name__, '=' * 75)
    banner = '#' * 80

    @wraps(view_func)
    def print_gap(*args, **kwargs):
        print title[:80]
        http_response = view_func(*args, **kwargs)
        print banner

        return http_response
    return print_gap

