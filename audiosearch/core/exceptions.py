from __future__ import absolute_import


class AudiosearchError(Exception):
    pass
    
class APIConnectionError(AudiosearchError):
    pass

class APIResponseError(AudiosearchError):
    pass

class RateLimitError(AudiosearchError):
    pass
