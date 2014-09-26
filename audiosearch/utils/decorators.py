from __future__ import absolute_import

from functools import wraps

from audiosearch.models import resources
from audiosearch import Cache


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
        print banner + '\n'

        return http_response
    return print_gap


def reset_cache(page):
    """
    Delete the keys associated with the requested page from cache before 
    executing the view.
    """
    def wrapper(view_func):
        def delete_key(*args, **kwargs):
            if page == 'top':
                key = resources.TopArtists().key
            else:
                key = None

            if key:
                banner = ' ' + ('!' * 2) + ' '
                print '\n{}Removing: {}{}'.format(banner, key, banner)
                Cache.delete(key)
            
            return view_func(*args, **kwargs)
        return wraps(view_func)(delete_key)
    return wrapper
