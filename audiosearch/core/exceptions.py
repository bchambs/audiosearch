from __future__ import absolute_import


class APIConnectionError(Exception):
    pass

class APIResponseError(Exception):
    pass

class RateLimitError(Exception):
    pass
