from __future__ import absolute_import

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
REDIS_TTL = 3000     # in seconds


################
# DATA DISPLAY #
################
SIM_ART_DISPLAYED = 100
ART_SONGS_DISPLAYED = 10
ITEMS_PER_SEARCH = 100
ITEMS_PER_PAGE = 10


#############
# DEBUGGING #
#############

# delete requested key from cache before serving request
REDIS_DEBUG = False

# print context before returning template
VIEW_DEBUG = False

# print echo nest response info
CONSUMER_DEBUG = False


