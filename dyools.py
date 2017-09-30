#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from contextlib import contextmanager

import click
import sys

__VERSION__ = '0.2.2'
__AUTHOR__ = ''
__WEBSITE__ = ''
__DATE__ = ''


class Eval(object):
    def __init__(self, data, context):
        self.data = data
        self.context = context or {}

    def eval(self, eval_result=True):
        def parse(value, ctx):
            if isinstance(value, list):
                return [parse(item, ctx) for item in value]
            elif isinstance(value, dict):
                _d = {}
                for _k, _v in value.items():
                    _d[_k] = parse(_v, ctx)
                return _d
            elif isinstance(value, basestring):
                origin = value
                res = value.format(**ctx)
                if origin != res and eval_result:
                    try:
                        res = eval(res, ctx)
                    except Exception as e:
                        pass
                return res
            else:
                return value

        return parse(self.data, self.context)


class SFTP(object):
    def __init__(self, sftp):
        self.sftp = sftp

    @contextmanager
    def chdir(self, path):
        try:
            origin = self.sftp.getcwd()
            self.sftp.chdir(path)
            yield
        except Exception as e:
            raise e
        finally:
            self.sftp.chdir(origin)


class Path(object):
    @classmethod
    @contextmanager
    def chdir(cls, path):
        try:
            origin = os.getcwd()
            os.chdir(path)
            yield
        except Exception as e:
            raise e
        finally:
            os.chdir(origin)

    @classmethod
    def subpaths(self, path, isfile=False):
        elements = []
        sep = os.path.sep if path.startswith(os.path.sep) else ''
        res = [x for x in path.split(os.path.sep) if x]
        res.reverse()
        while res:
            item = res.pop()
            if elements:
                elements.append(os.path.join(sep, elements[-1], item))
            else:
                elements = [os.path.join(sep, item)]
        return elements if not isfile else elements[:-1]


class Logger(object):
    def info(self, msg):
        click.echo(msg)

    def warn(self, msg):
        click.secho(msg, fg='yellow')

    def debug(self, msg):
        click.secho(msg, fg='blue')

    def success(self, msg):
        click.secho(msg, fg='green')

    def code(self, msg):
        click.secho(msg, fg='cyan')

    def error(self, msg):
        click.secho(msg, fg='red')
        sys.exit(-1)

    def title(self, msg):
        click.secho(msg, fg='white', bold=True)


if __name__ == '__main__':
    # l = Logger()
    # l.title('Title')
    # l.info('Info')
    # l.warn('Warn')
    # l.debug('Debug')
    # l.success('Success')
    # l.code('Code')
    #
    # l.info(os.getcwd())
    # with Path.chdir('/'):
    #     l.warn(os.getcwd())
    # l.info(os.getcwd())


    # from pprint import pprint
    #
    # pprint(Path.subpaths('/hh/k/l/mmmmmm/TTT', True))
    # l.error('Error')
    # l.error('Ooops')
    s = {
        1: 9,
        '1': '9',
        'j': [1, 3, 5],
        'r': [1, {'g': 'vv {med}'}, {5: {8: [{'z': '{nbr}'}]}}],
    }
    ctx = {
        'med': 'MED',
        'nbr': 4,
    }
    res1 = Eval(s, ctx).eval(eval_result=True)
    res2 = Eval(s, ctx).eval(eval_result=False)
    from pprint import pprint

    pprint(res1)
    pprint(res2)
