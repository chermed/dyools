from __future__ import (absolute_import, division, print_function, unicode_literals)

from .klass_if import IF


class Operator(object):
    @classmethod
    def flat(cls, *lists):
        result = []

        def put_in(item):
            if IF.is_iterable(item):
                for x in item:
                    put_in(x)
            else:
                result.append(item)

        for item in lists:
            put_in(item)
        return result

    @classmethod
    def unique(cls, sequence):
        result = []
        if IF.is_iterable(sequence):
            for item in sequence:
                found = False
                for res in result:
                    if res is item:
                        found = True
                        break
                if not found:
                    result.append(item)
        else:
            return sequence
        return result

    @classmethod
    def split_and_flat(cls, sep=',', *lists):
        result = cls.flat(lists)
        for i, item in enumerate(result):
            if IF.is_str(item):
                result[i] = item.split(sep)
        return cls.flat(result)

        def put_in(item):
            if IF.is_iterable(item):
                for x in item:
                    put_in(x)
            else:
                result.append(item)

        for item in lists:
            put_in(item)
        return result
