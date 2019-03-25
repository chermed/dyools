from __future__ import (absolute_import, division, print_function, unicode_literals)

import sys

import click

from .klass_data import Data
from .klass_xml import XML


@click.group(invoke_without_command=True)
@click.option('--attrs', '-a', type=click.STRING, nargs=2, multiple=True)
@click.option('--tags', '-t', type=click.STRING, nargs=1, multiple=True)
@click.option('--separator', '-s', type=click.STRING, default=XML.SEPARATOR, )
@click.option('--with-arch', is_flag=True, default=False)
def cli_xml(attrs, tags, separator, with_arch):
    attrs, tags = dict(attrs), list(tags)
    clean_arch = ''
    arch = ''
    for line in sys.stdin:
        arch += '\n{}'.format(line)
    if arch.count(separator) == 2:
        ok = False
        for line in arch.split('\n'):
            if line.strip() == separator.strip():
                if not ok:
                    ok = True
                    continue
                else:
                    break
            if ok:
                clean_arch += line + '\n'
    else:
        clean_arch = arch
    if with_arch:
        Data(XML(clean_arch).expr_with_arch(*tags, **attrs)).show()
    else:
        Data(XML(clean_arch).expr(*tags, **attrs)).show()
