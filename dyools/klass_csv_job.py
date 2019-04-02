from __future__ import (absolute_import, division, print_function, unicode_literals)

import logging

from .klass_odoo_job import OdooJob

logger = logging.getLogger(__name__)


class CsvJob(OdooJob):

    def get(self, put_method, queue_data):
        fcsv = self.get_source()
        data = []
        for i, line in enumerate(fcsv):
            if self.limit and i < self.offset:
                continue
            if self.limit and i >= self.offset and i == self.limit+self.offset:
                break
            data.append(dict(line))
        queue_data.append((put_method, data))

    def count(self):
        return sum(1 for _ in self.get_source())
