"""
Audiosearch constants.
"""

#############
# ECHO NEST #
#############
API_KEY = "QZQG43T7640VIF4FN"
CALL_SNOOZE = 1     # in seconds
CALL_TIMEOUT = 15
CALL_LIMIT = 15
RESULTS = 100


##########
# CELERY #
##########


#########
# REDIS #
#########
REDIS_TTL = 3000    # in seconds
SIZE_LIMIT = 100    # max keys allowed in cache



################
# DATA DISPLAY #
################
ARTISTS_IN_GRID = 9
ITEMS_PER_PAGE = 10
GENRE_COUNT = 5
EMPTY_MSG = "Your search did not match any music data."
NO_DATA_MSG = "We could not find data for this item."


#############
# DEBUGGING #
#############
DEBUG_TOOLBAR = True

