from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
import re

from past.builtins import basestring

from .decorators import raise_exception
from .klass_eval import Eval

builtin_dict = dict
builtin_list = list
builtin_tuple = tuple


class IS(object):
    @classmethod
    @raise_exception(exception=TypeError, exception_msg='[%s] is not an XML-ID valid', arg_index=1)
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
    @raise_exception(exception=TypeError, exception_msg='[%s] is not a domain', arg_index=1)
    def domain(cls, text):
        if not isinstance(text, builtin_list):
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
    @raise_exception(exception=TypeError, exception_msg='[%s] is not a string', arg_index=1)
    def str(cls, text):
        if isinstance(text, basestring):
            return True
        else:
            return False

    @classmethod
    @raise_exception(exception=TypeError, exception_msg='[%s] is not a list', arg_index=1)
    def list(cls, text):
        if isinstance(text, builtin_list):
            return True
        else:
            return False

    @classmethod
    @raise_exception(exception=TypeError, exception_msg='[%s] is not a dict', arg_index=1)
    def dict(cls, text):
        if isinstance(text, builtin_dict):
            return True
        else:
            return False

    @classmethod
    @raise_exception(exception=TypeError, exception_msg='[%s] is not a tuple', arg_index=1)
    def tuple(cls, text):
        if isinstance(text, tuple):
            return True
        else:
            return False

    @classmethod
    @raise_exception(exception=TypeError, exception_msg='[%s] is not empty', arg_index=1)
    def empty(cls, text):
        if cls.str(text):
            text = text.strip()
        if text:
            return False
        else:
            return True

    @classmethod
    @raise_exception(exception=TypeError, exception_msg='[%s] is not iterable', arg_index=1)
    def iterable(cls, text):
        if cls.str(text):
            return False
        if hasattr(text, '__iter__'):
            return True
        else:
            return False

    @classmethod
    @raise_exception(exception=TypeError, exception_msg='[%s] can not be evaluated', arg_index=1)
    def eval(cls, text, ctx={}):
        if not isinstance(text, basestring):
            return False
        try:
            dest = Eval(text, ctx).eval()
            if dest != text:
                return True
        except:
            pass
        return False

    @classmethod
    @raise_exception(exception=TypeError, exception_msg='[%s] is not list or tuple', arg_index=1)
    def list_or_tuple(cls, item):
        return isinstance(item, (builtin_list, builtin_tuple))

    @classmethod
    @raise_exception(exception=TypeError, exception_msg='[%s] is not list of list', arg_index=1)
    def list_of_list(cls, item):
        if not isinstance(item, builtin_list):
            return False
        if not item:
            return True
        if not isinstance(item[0], builtin_list):
            return False
        return True

    @classmethod
    @raise_exception(exception=TypeError, exception_msg='[%s] is not a list of values', arg_index=1)
    def list_of_values(cls, item):
        if not isinstance(item, builtin_list):
            return False
        if not item:
            return True
        if isinstance(item[0], (builtin_dict, builtin_list)):
            return False
        return True

    @classmethod
    @raise_exception(exception=TypeError, exception_msg='[%s] is not list of dictionaries', arg_index=1)
    def list_of_dict(cls, item):
        if not isinstance(item, builtin_list):
            return False
        if not item:
            return True
        if not isinstance(item[0], builtin_dict):
            return False
        return True

    @classmethod
    @raise_exception(exception=TypeError, exception_msg='[%s] is not a dictionary of dictionaries', arg_index=1)
    def dict_of_dict(cls, item):
        if not isinstance(item, builtin_dict):
            return False
        for k, v in item.items():
            if isinstance(v, builtin_dict):
                return True
            else:
                return False
        return True

    @classmethod
    @raise_exception(exception=TypeError, exception_msg='[%s] is not a list of values', arg_index=1)
    def dict_of_values(cls, item):
        if not isinstance(item, builtin_dict):
            return False
        for k, v in item.items():
            if isinstance(v, builtin_dict):
                return False
            else:
                return True
        return True

    @classmethod
    @raise_exception(exception=FileNotFoundError, exception_msg='[%s] not found or is not a file', arg_index=1)
    def file(cls, item):
        if os.path.isfile(item):
            return True
        else:
            return False

    @classmethod
    @raise_exception(exception=NotADirectoryError, exception_msg='[%s] not found or is not a directory', arg_index=1)
    def dir(cls, item):
        if os.path.isdir(item):
            return True
        else:
            return False
