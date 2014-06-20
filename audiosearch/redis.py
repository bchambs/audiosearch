from __future__ import absolute_import
import redis

global client

pool = redis.ConnectionPool(max_connections=100)
client = redis.StrictRedis(host='localhost', port=6379, db=0, connection_pool=pool)
client.client_setname('django_redis_client')
