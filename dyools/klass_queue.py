from __future__ import (absolute_import, division, print_function, unicode_literals)

import logging
from queue import Queue
from threading import Thread

logger = logging.getLogger(__name__)


class Queue(Queue):
    def __init__(self, name, maxsize=0, output_queue=None):
        super(Queue, self).__init__(maxsize=maxsize)
        self.name = name
        self.output_queue = output_queue

    def start(self):
        logger.info('queue: name=%s processing is started, output name=%s', self.name,
                    getattr(self.output_queue, 'name', None))
        while True:
            received_data = self.get()
            if received_data is None:
                logger.info('queue: name=%s receive stop signal', self.name)
                if self.output_queue:
                    self.output_queue.put(received_data)
                break
            len_received_data = len(received_data)
            logger.info('queue: name=%s start to process datas threads=%s', self.name, len_received_data)
            tab = []
            queue_data = []
            for i in range(len_received_data):
                methods, data = received_data[i]
                print(self.name, methods, data)
                i += 1
                t = Thread(target=methods[0], args=(methods[1:], queue_data))
                t.start()
                tab.append(t)
            self.task_done()
            for t in tab:
                t.join()
            if self.output_queue :
                self.output_queue.put(queue_data)
            logger.info('queue: name=%s end portion from %s threads', self.name, len_received_data)
