#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from contextlib import contextmanager

import click
import sys

__VERSION__ = '0.2.1'
__AUTHOR__ = ''
__WEBSITE__ = ''
__DATE__ = ''


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
    l = Logger()
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


    from pprint import pprint
    pprint(Path.subpaths('/hh/k/l/mmmmmm/TTT', True))
    # l.error('Error')
    # l.error('Ooops')
