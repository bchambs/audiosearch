import event_queue
import threading

__all__ = ['Worker']

class Worker(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue

    def run(self):
        while True:
            request = self.queue.dequeue()
            print 'dequeueuing: ', self.queue._queue.qsize()
            request.serve()
            self.queue._queue.task_done()
            