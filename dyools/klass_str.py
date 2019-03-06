from __future__ import (absolute_import, division, print_function, unicode_literals)

import unicodedata


class Str(object):
    def __init__(self, arg):
        self.arg = '{}'.format(arg)

    def to_code(self):
        txt = self.arg.strip()
        txt = [x for x in txt if x.isalnum() or x == ' ']
        txt = ''.join(txt)
        txt = '_'.join(txt.strip().upper().split())
        txt = [c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn']
        txt = ''.join(txt)
        return txt

    def remove_spaces(self):
        return self.arg.replace(' ', '')

    def remove_accents(self):
        txt = self.arg
        txt = [c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn']
        txt = ''.join(txt)
        return txt

    def to_str(self):
        return '{}'.format(self.arg)

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()