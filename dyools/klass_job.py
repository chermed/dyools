from __future__ import (absolute_import, division, print_function, unicode_literals)

import abc


class Job(object, metaclass=abc.ABCMeta):
    _source = False
    _destination = False

    def __init__(self, **kwargs):
        if not all([self._source, self._destination]):
            raise Exception(
                "A Job subclass should define _source and _destination static variables")
        for k, v in kwargs.items():
            if isinstance(k, str) and not k.startswith('_'):
                setattr(self, k, v)
        self.context = kwargs

    def get_source(self):
        return self.context[self._source]()

    def get_destination(self):
        return self.context[self._destination]()

    @abc.abstractmethod
    def transform(self, data):
        pass
