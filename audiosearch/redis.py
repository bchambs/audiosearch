from __future__ import absolute_import

import redis

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
EXPIRE_TIME = 2


"""
----------------------
Establish Redis client
----------------------
"""

pool = redis.ConnectionPool(max_connections=CONNECTIONS)
client = redis.StrictRedis(host=HOST, port=PORT, db=DATABASE, connection_pool=pool)
client.client_setname('django_redis_client')
