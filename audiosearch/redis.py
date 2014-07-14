from __future__ import absolute_import

import redis

"""
------
Schema
------

Key = artist, song, playlist... id
Values by type:
    Artist = {
        status = {
            'profile': string,
            'songs': string,
            'similar': string
        }

        profile = {
            'bio_full': string
            'bio_trunc': string
            'tiles': list of (string, url) tuple
            'terms': string
            'hotttnesss': float
        }
        songs = list of dict
        similar = list of dict
    }
    Song = {
        status = {
            'profile': string,
        }

        profile = {
            'audio_summary': dict
            'song_hotttnesss': float
            'song_hotttnesss_rank': float
        }
    }
"""

"""
---------------
Redis constants
---------------
"""

HOST = 'localhost'
PORT = 6379
DATABASE = 0
CONNECTIONS = 20

# in seconds
EXPIRE_TIME = 300

"""
----------------------
Redis client
----------------------
"""

pool = redis.ConnectionPool(max_connections=CONNECTIONS)
client = redis.StrictRedis(host=HOST, port=PORT, db=DATABASE, connection_pool=pool)
client.client_setname("django_redis_client")
