# Echo Nest API.
API_KEY = "QZQG43T7640VIF4FN"
CALL_SNOOZE = 1     # In seconds.
CALL_TIMEOUT = 15
CALL_LIMIT = 15
RESULTS = 100


# Redis cache.
STANDARD_TTL = 3000     # In seconds.
PERSIST = 0             # Does not expire.
EMPTY = "::EMPTY::"
FAILED = "::FAILED::"
PENDING = "::PENDING::"


# Trending.
T_HASH = "trending:hash"
T_CONTENT = "trending:content"
T_MIN ="trending:min"
# T_COUNT = 15 # Number of items to track in /trending/.


# Data display.
N_CONTENT_ROWS = 10
GENRE_COUNT = 5
# EMPTY_MSG = "Your search did not match any music data."
# NO_DATA_MSG = "We could not find data for this item."
SERVICE_TIMOUT_MSG = "Audiosearch is receiving too many requests.  Try again soon!"


# Redis-content map.
HASH_ = DICT_ = "dictionary"
LIST_ = "list"
STRING_ = STR_ = "string"
