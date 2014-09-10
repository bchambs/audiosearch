from __future__ import absolute_import

from functools import wraps
    

def stdout_gap(view_func):
    """
    Visual cue for view debugging.  Seperates view function 'print's from the
    django test server HTTP response spam.
    """
    before = "\n{}".format('#' * 80)
    after = before[::-1]

    @wraps(view_func)
    def print_gap(*args, **kwargs):
        print before
        http_response = view_func(*args, **kwargs)
        print after

        return http_response
    return print_gap
