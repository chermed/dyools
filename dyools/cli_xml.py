from __future__ import (absolute_import, division, print_function, unicode_literals)

import click


@click.group(invoke_without_command=True)
@click.argument('input', type=click.STRING, nargs=-1)
@click.option('--attrs', '-a', type=click.STRING, nargs=2, multiple=True)
@click.option('--tags', '-t', type=click.STRING, nargs=1, multiple=True)
def cli_xml(input, attrs, tags):
    clean_arch = ''
    if arch.count(SEPARATOR) >= 2:
        for line in arch.split('\n'):
            ok = False
            if line == SEPARATOR and not ok:
                ok = True
                continue
            if ok :
                clean_arch += line + '\n'


