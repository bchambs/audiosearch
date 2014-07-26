from __future__ import absolute_import

import redis


HOST = 'localhost'
PORT = 6379
DATABASE = 0
CONNECTIONS = 20

pool = redis.ConnectionPool(max_connections=CONNECTIONS)
client = redis.StrictRedis(host=HOST, port=PORT, db=DATABASE, connection_pool=pool)
client.client_setname("django_redis_client")
