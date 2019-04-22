from __future__ import (absolute_import, division, print_function, unicode_literals)

import click
from faker import Faker

from .klass_data import Data
from .klass_print import Print
from .klass_random import Random


@click.group()
def cli_tool():
    pass


@cli_tool.command('random')
@click.argument('length', type=click.INT, default=24, required=False)
@click.option('--nbr', '-n', type=click.INT, default=1, required=False, help='Number of random to generate')
@click.option('--uuid', is_flag=True, type=click.BOOL, default=False, required=False, help='Show UUID')
@click.option('--base64', is_flag=True, type=click.BOOL, default=False, required=False,
              help='Show a random string of base64')
@click.option('--alpha', is_flag=True, type=click.BOOL, default=False, required=False,
              help='Show a random string of alpha characters')
@click.option('--digits', is_flag=True, type=click.BOOL, default=False, required=False,
              help='Show a random string of digits')
@click.option('--alphanum', is_flag=True, type=click.BOOL, default=False, required=False,
              help='Show a random string of alphanumerics')
def __random(length, nbr, uuid, base64, alpha, digits, alphanum):
    """Generate random strings"""
    Print.info('Some random strings')
    if not any([uuid, base64, alpha, digits, alphanum]):
        uuid = base64 = alpha = digits = alphanum = True
    tab = []
    for i in range(nbr):
        i += 1
        if uuid:
            tab.append([i, 'uuid', Random.uuid()])
        if base64:
            tab.append([i, 'base64', Random.base64(length)])
        if alpha:
            tab.append([i, 'alpha', Random.alpha(length)])
        if digits:
            tab.append([i, 'digits', Random.digits(length)])
        if alphanum:
            tab.append([i, 'alphanum', Random.alphanum(length)])
    Data(tab, header=['Index', 'Name', 'Value']).show()


@cli_tool.command('fake')
@click.argument('name', type=click.STRING, required=False)
@click.option('--keys', is_flag=True, default=False, help='Show just keys', )
def __fake(name, keys):
    """Show a fake examples"""
    fake = Faker('fr_FR')
    for attr in dir(fake):
        if not attr.startswith('_'):
            if name and (name not in attr and attr not in name):
                continue
            try:
                Print.info('{:.<30}{}'.format(attr, getattr(fake, attr)() if not keys else '*'))
            except:
                pass
