from __future__ import (absolute_import, division, print_function, unicode_literals)

import logging
import time
from queue import Queue as pyQueue
from threading import Thread

logger = logging.getLogger(__name__)

class Queue(object):
    def __init__(self, maxsize=0):
        self._stop = False
        self._data = {}
        self._to_send = {}
        self._py_queue = pyQueue(maxsize=maxsize)

    def push(self, index):
        self._py_queue.put(index)

    def qsize(self):
        return self._py_queue.qsize()

    def get_next_index(self, timeout=1, default=0):
        try:
            return self._py_queue.get(timeout=timeout)
        except:
            return default

    def add(self, priority, threads, total):
        self._to_send[priority] = [threads, total]

    def append(self, priority, put_method, item):
        self._data.setdefault(priority, [])
        self._data[priority].append([put_method, item])

    def remove(self, priority):
        self._data.pop(priority)

    def stop(self, wait=2):
        time.sleep(wait)
        self._stop = True

    def start(self):
        logger.info('queue: processing is started')
        last_index = 0
        while True:
            index = self.get_next_index(default=0)
            if index:
                if last_index and index > last_index:
                    del self._to_send[index]
                    del self._data[index]
                last_index = index
                jobs = self._data[index]
                queue_threads, len_queue_priority = self._to_send[index]
                queue_threads = min([queue_threads, len_queue_priority])
                logger.info('queue: start to process priority=%s threads=%s',index, queue_threads)
                tab = []
                for i in range(queue_threads):
                    put_method, data = jobs[i]
                    i += 1
                    t = Thread(target=put_method, args=(data,))
                    t.start()
                    tab.append(t)
                for t in tab:
                    t.join()
                logger.info('queue: end portion of the priority %s', index)
            if not index and self._stop:
                logger.info('queue: receive stop signal')
                break
