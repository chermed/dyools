from __future__ import (absolute_import, division, print_function, unicode_literals)

import logging
import time
from queue import Queue as pyQueue
from threading import Thread

logger = logging.getLogger(__name__)

class Queue(object):
    def __init__(self):
        self._stop = False
        self.sender_index = 0
        self._data = {}
        self._to_send = {}
        self._py_queue = pyQueue()

    def push(self, index):
        self._py_queue.put(index)

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

    def send(self):
        while True:
            receiver_index = self.get_next_index(default=0)
            if receiver_index:
                if not self.sender_index:
                    self.sender_index =receiver_index
            if receiver_index and self.sender_index < receiver_index:
                logger.info('sender: start to process the priority [%s]' % self.sender_index)
                jobs = self._data[self.sender_index]
                queue_threads, len_queue_priority = self._to_send[self.sender_index]
                queue_threads = min([queue_threads, len_queue_priority])
                index = 0
                while index < len_queue_priority:
                    logger.info('sender: stage priority=%s %s-%s/%s',self.sender_index, index, queue_threads + index, len_queue_priority)
                    tab = []
                    for i in range(queue_threads):
                        put_method, data = jobs[index]
                        index += 1
                        t = Thread(target=put_method, args=(data,))
                        t.start()
                        tab.append(t)
                    for t in tab:
                        t.join()
                    queue_threads = min([queue_threads, len(jobs[index:])])
                logger.info('sender: complete the priority %s move to %s', self.sender_index, receiver_index)
                self.sender_index = receiver_index

            if not receiver_index and self._stop:
                self.sender_index = receiver_index
                logger.info('sender: receive stop signal')
                break
