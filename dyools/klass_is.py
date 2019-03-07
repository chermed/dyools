from __future__ import (absolute_import, division, print_function, unicode_literals)

import re

from past.builtins import basestring


class IS(object):
    @classmethod
    def xmlid(cls, text):
        if not cls.str(text) or cls.empty(text):
            return False
        else:
            text = text.strip()
            if re.match("^[a-z0-9_]+\.[a-z0-9_]+$", text):
                return True
            else:
                return False

    @classmethod
    def domain(cls, text):
        if not isinstance(text, list):
            return False
        ttuple, op = 0, 0
        for item in text:
            if isinstance(item, tuple):
                ttuple += 1
                if not (len(item) == 3 and isinstance(item[0], basestring) and isinstance(item[1], basestring)):
                    return False
            elif isinstance(item, basestring):
                op += 1
                if item not in ['&', '|', '!']:
                    return False
            else:
                return False
        if (op or ttuple) and op >= ttuple:
            return False
        return True

    @classmethod
    def str(cls, text):
        if isinstance(text, basestring):
            return True
        else:
            return False

    @classmethod
    def empty(cls, text):
        if cls.str(text):
            text = text.strip()
        if text:
            return False
        else:
            return True

    @classmethod
    def iterable(cls, text):
        if cls.str(text):
            return False
        if hasattr(text, '__iter__'):
            return True
        else:
            return False
