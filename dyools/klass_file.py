from __future__ import (absolute_import, division, print_function, unicode_literals)

import os


class File(object):
    @classmethod
    def get_size_str(cls, path, unit='mb'):
        size, u = cls._get_size(path, unit=unit)
        return "%s %s" % (size, u)

    @classmethod
    def get_size(cls, path, unit='mb'):
        size, u = cls._get_size(path, unit=unit)
        return size

    @classmethod
    def _get_size(cls, path, unit='mb'):
        size = os.path.getsize(path)
        if unit == 'mb':
            return round(size / (1024. * 1024.), 2), 'MB'
        else:
            return round(size, 2), 'B'
