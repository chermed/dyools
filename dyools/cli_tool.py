from __future__ import (absolute_import, division, print_function, unicode_literals)

import base64 as pkg_base64
import os
import random as pkg_random
import string as pkg_string
import uuid as pkg_uuid

import click
from faker import Faker

from .klass_data import Data
from .klass_print import Print


@click.group()
def cli_tool():
    pass


@cli_tool.command('random')
@click.argument('length', type=click.INT, default=24, required=False)
@click.option('--nbr', '-n', type=click.INT, default=1, required=False)
@click.option('--uuid', is_flag=True, type=click.BOOL, default=False, required=False)
@click.option('--base64', is_flag=True, type=click.BOOL, default=False, required=False)
def __random(length, nbr, uuid, base64):
    """Generate random strings"""
    Print.info('Some random strings')
    tab = []
    for i in range(nbr):
        if uuid:
            generated_string = str(pkg_uuid.uuid1())
        elif base64:
            generated_string = pkg_base64.b64encode(os.urandom(length))
        else:
            generated_string = ''.join(
                pkg_random.choice(pkg_string.ascii_letters + pkg_string.digits) for _ in range(length))
        tab.append([generated_string])
    Data(tab, header=['String']).show()


@cli_tool.command('fake')
@click.argument('name', type=click.STRING, required=False)
@click.option('--keys', is_flag=True, default=False)
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
