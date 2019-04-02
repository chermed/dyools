from __future__ import (absolute_import, division, print_function, unicode_literals)

import logging
import time
from queue import Queue as pyQueue
from threading import Thread

logger = logging.getLogger(__name__)

class Queue(object):
    def __init__(self, maxsize=0):
        self._stop = False
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

    def stop(self, wait=2):
        time.sleep(wait)
        self._stop = True

    def start(self):
        logger.info('queue: processing is started')
        while True:
            queue_data = self.get_next_index(default=0)
            if queue_data:
                len_queue_data = len(queue_data)
                logger.info('queue: start to process datas threads=%s',len_queue_data)
                tab = []
                for i in range(len_queue_data):
                    put_method, job_data = queue_data[i]
                    i += 1
                    t = Thread(target=put_method, args=(job_data,))
                    t.start()
                    tab.append(t)
                for t in tab:
                    t.join()
                logger.info('queue: end portion from %s threads', len_queue_data)
            if not queue_data and self._stop:
                logger.info('queue: receive stop signal')
                break
