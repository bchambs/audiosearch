"""
TODO: move to /audiosearch/conf/global_settings.py or remove need for globals.
"""
# Echo Nest API.
API_KEY = 'QZQG43T7640VIF4FN'
CALL_SNOOZE = 1         # In seconds.


# Redis cache.


# Cache key status codes.
AVAIL = 'available'
FAIL = 'failed'
NEW = 'new'
PEND = 'pending'


# Trending.
T_HASH = 'trending:hash'
T_CONTENT = 'trending:content'
T_MIN ='trending:min'
# T_COUNT = 15 # Number of items to track in /trending/.


# Data display.
N_CONTENT_ROWS = 10
N_GENRE_TAGS = 5


# Messages.
MSG_SERVICE_TIMOUT = "Audiosearch is receiving too many requests.  Try again soon!"
MSG_NO_SEARCH_DATA = "Your search did not match any music data."
MSG_NO_DATA = "We could not find data for this item."
MSG_UNEXPECTED_STORAGE_TYPE = "Unexpected data type received."
