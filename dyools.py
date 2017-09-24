#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import sys

__VERSION__ = '0.1.1'
__AUTHOR__ = ''
__WEBSITE__ = ''
__DATE__ = ''


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
    l.title('Title')
    l.info('Info')
    l.warn('Warn')
    l.debug('Debug')
    l.success('Success')
    l.code('Code')
    l.error('Error')
    l.error('Ooops')
