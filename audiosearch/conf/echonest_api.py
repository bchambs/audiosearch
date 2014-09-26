from __future__ import absolute_import


# Path dirs
API = 'api'
VERSION = 'v4'

# URL
PROTOCOL = 'http'
HOST = '://developer.echonest.com'
BASE_PATH = '/'.join([API, VERSION])
BASE_URL = '/'.join([PROTOCOL, HOST, BASE_PATH])

# Required payload
KEY = 'QZQG43T7640VIF4FN'
FORMAT = 'json'
BASE_PARAMS = {
    'api_key': KEY,
    'format': FORMAT,
}

# Largest size of a data element in response
MAX_RESULTS = 100   

# Number of genre tags displayed in artist profiles (move to display ?)
GENRE_COUNT = 5
