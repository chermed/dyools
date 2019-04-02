from __future__ import (absolute_import, division, print_function, unicode_literals)

import logging

from .klass_is import IS
from .klass_job import Job
from .klass_str import Str

logger = logging.getLogger(__name__)


class OdooJob(Job):
    _name = False
    _source_name = False
    _destination_name = False
    _fields = False
    _source_fields = False
    _destination_fields = False

    def __init__(self, **kwargs):
        if not all([self._name, self._fields]):
            raise Exception(
                "An OdooJob subclass should define the static variables : _name, _fields")
        if not self._source_fields:
            self._source_fields = self._fields
        if not self._destination_fields:
            self._destination_fields = self._fields
        if not self._source_name:
            self._source_name = self._name
        if not self._destination_name:
            self._destination_name = self._name
        super(OdooJob, self).__init__(**kwargs)

    def get(self, put_method, queue_data):
        odoo = self.get_source()
        ids = odoo.env[self._source_name].search(self.domain, offset=self.offset, limit=self.limit)
        queue_data.append((put_method, odoo.env[self._source_name].read(ids, self._source_fields)))

    def put(self, data):
        data = self.transform(data)
        odoo = self.get_destination()
        if self.context.get('primary_keys'):
            logger.info('sender: odoojob use create/write based on fields = %s' % self.context['primary_keys'])
            for record in data:
                domain = [(pk, '=', record[pk]) for pk in self.context['primary_keys']]
                ids = odoo.env[self._destination_name].search(domain)
                if ids:
                    odoo.env[self._destination_name].write(ids, record)
                else:
                    ids = odoo.env[self._destination_name].create(record)
                if not ids:
                    return False
        else:
            fields, data = self._generic_transform(odoo, data)
            logger.info('sender: odoojob use load model=%s fields=%s', self._destination_name, fields)
            logger.debug('sender: odoojob call load with fields=%s data=%s', fields, data)
            if not odoo.env[self._destination_name].load(fields, data):
                return False
        return True

    def transform(self, data):
        return data

    def _generic_transform(self, odoo, read_data):
        ffield = odoo.env[self._destination_name].fields_get()
        load_data = []
        fields = []
        if read_data:
            fields = list(read_data[0].keys())
            fields = [x for x in fields if x in self._destination_fields]
        for record in read_data:
            line = []
            for f in fields:
                if f == 'id':
                    record[f] = Str(record[f]).to_code().lower()
                    line.append('__migration__.%s_%s' % (Str(self._source_name).dot_to_underscore(), record[f]))
                    continue
                if IS.iterable(record[f]) and len(record[f]) == 2:
                    line.append('__migration__.%s_%s' % (Str(ffield[f]).dot_to_underscore(), record[f][0]))
                    continue
                if IS.iterable(record[f]):
                    _res = []
                    for item in record[f]:
                        _res.append('__migration__.%s_%s' % (Str(ffield[f]).dot_to_underscore(), item))
                    line.append(','.join(_res))
                    continue
                line.append(record[f])
            load_data.append(line)
        return fields, load_data

    def count(self):
        return self.get_source().env[self._source_name].search_count([])
