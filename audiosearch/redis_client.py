from __future__ import absolute_import

import redis

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audiosearch.settings')

redis = redis.StrictRedis(host='localhost', port=6379, db=0)