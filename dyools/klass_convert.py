from __future__ import (absolute_import, division, print_function, unicode_literals)


class Convert(object):
    def __init__(self, arg={}):
        self.data = arg

    @classmethod
    def data(self, amount, origin, to):
        units = ["B", "K", "M", "G", "T", "P", "E", "Z", "Y"]
        origin, to = origin.strip().upper()[0], to.strip().upper()[0]
        assert origin in units and to in units, 'The units are not mapped'
        i = 0
        while origin != units[i]:
            amount *= 2 ** 10
            i += 1
        i = 0
        while to != units[i]:
            amount /= 2 ** 10
            i += 1
        return amount
