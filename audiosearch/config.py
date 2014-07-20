from __future__ import absolute_import

"""
Audiosearch constants.
"""

#############
# ECHO NEST #
#############
API_KEY = "QZQG43T7640VIF4FN"


##########
# CELERY #
##########
CALL_SNOOZE = 1     # in seconds
CALL_TIMEOUT = 15


#########
# REDIS #
#########
REDIS_TTL = 300     # in seconds


################
# DATA DISPLAY #
################
SIM_ART_DISPLAYED = 10
ART_SONGS_DISPLAYED = 10
ITEMS_PER_SEARCH = 15
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
