from Queue import *

# queue of artist or song ids
class EventQueue:
    def __init__(self):
        self._queue = Queue()
        self._worker = Worker()

    def enqueue(self, req_id):
        self._queue.put(req_id)

    def dequeue(self):
        return self._queue.get()

    class Worker:
        