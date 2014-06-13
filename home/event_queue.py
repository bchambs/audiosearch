from Queue import *

__all__ = ['EventQueue']

# queue of artist or song ids
class EventQueue:
    def __init__(self):
        self._queue = Queue()

    def enqueue(self, req_id):
        self._queue.put(req_id)
        print 'enqueueuing: ', self._queue.qsize()

    def dequeue(self):
        return self._queue.get()
