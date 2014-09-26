"""Abstract task class definitions and mixins."""

from __future__ import absolute_import
import os

from celery import Task

from audiosearch.cache.redis import RedisCache
from audiosearch.conf import settings


class SharedConnection(Task):
    """Enforce all tasks executed in a worker's subprocess to use the same
    audiosearch cache client.
    """
    abstract = True
    _cache = None


    @property
    def Cache(self):
        if self._cache is None:
            pid = os.getpid()
            worker_subprocess = 'worker @ {}'.format(pid)
            self._cache = RedisCache(worker_subprocess, settings.CACHE_CONFIG)
        return self._cache



