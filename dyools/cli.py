from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
from os.path import expanduser

import click

from .klass_yaml_config import YamlConfig

home = expanduser("~")
home = os.path.join(home, '.dyvz')

CONFIG_FILE = os.path.join(home, 'dyools.yml')

DEFAULT_CONFIG = {
    'host': 'localhost',
    'port': 8069,
    'database': 'demo',
    'user': 'admin',
    'password': 'admin',
    'superadminpassword': 'admin',
    'protocol': 'jsonrpc',
    'mode': 'dev',
    'default': False,
}


@click.group()
@click.option('--database', '-d', type=click.STRING, default=None, help="Database")
@click.option('--host', '-h', type=click.STRING, default=None, help="Host")
@click.option('--load', '-l', type=click.STRING, help="Name")
@click.option('--prompt-login', type=click.BOOL, is_flag=True, help="Prompt the Odoo parameters for loggin")
@click.option('--prompt-connect', type=click.BOOL, is_flag=True, help="Prompt the Odoo parameters for connection")
@click.option('--config', '-c',
              type=click.Path(
                  exists=True,
                  file_okay=True,
                  dir_okay=False,
                  writable=True,
                  readable=True,
                  resolve_path=True
              ), default=CONFIG_FILE, help="Path of the configuration")
@click.option('--port', '-p', type=click.INT, default=None, help="Port")
@click.option('--user', '-u', type=click.STRING, default=None, help="User")
@click.option('--password', '-pass', type=click.STRING, default=None, help="Password")
@click.option('--superadminpassword', '-s', type=click.STRING, default=None, help="Super admin password")
@click.option('--protocol', type=click.Choice(['jsonrpc+ssl', 'jsonrpc']), default=None, help="Protocol")
@click.option('--mode', '-m', type=click.Choice(['test', 'dev', 'prod']), default=None, help="Mode")
@click.option('--timeout', '-t', type=click.INT, default=60, help="Timeout in minutes")
@click.option('--yes', is_flag=True, default=False)
@click.option('--no-context', is_flag=True, default=False)
@click.option('--debug', is_flag=True, default=False)
@click.option('--workers', '-w', type=click.INT, default=0)
@click.pass_context
def cli(ctx, database, host, port, user, password, superadminpassword, protocol, timeout, config, load, mode,
        prompt_login, prompt_connect, yes, no_context, debug, workers):
    print(database, host, port, user, password, superadminpassword, protocol, timeout, config, load, mode,
          prompt_login, prompt_connect, yes, no_context, debug, workers)
    yaml_obj = YamlConfig(config)
    default_config = yaml_obj.get(default=True) or DEFAULT_CONFIG
    ctx.obj = {}
    ctx.obj['yaml_obj'] = yaml_obj
    ctx.obj['default_config'] = default_config


@cli.command('create')
@click.argument('name')
@click.pass_context
def __create_config(ctx, name):
    """Create a new configuration"""
    configs = ctx.obj['configs']
    host = click.prompt('host', default=DEFAULT_CONFIG['host'], type=str)
    port = click.prompt('port', default=DEFAULT_CONFIG['port'], type=str)
    database = click.prompt('database', default=DEFAULT_CONFIG['database'], type=str)
    user = click.prompt('user', default=DEFAULT_CONFIG['user'], type=str)
    password = click.prompt('password', default=DEFAULT_CONFIG['password'], type=str)
    superadminpassword = click.prompt('superadminpassword', default=DEFAULT_CONFIG['superadminpassword'], type=str)
    protocol = click.prompt('protocol', default=DEFAULT_CONFIG['protocol'], type=str)
    mode = click.prompt('mode', default=DEFAULT_CONFIG['mode'], type=str)
    print('CREATE', name)
    print('CREATE', host, port, database)


@cli.command('list')
@click.pass_context
def __list(ctx):
    """Command line for dyools"""
    print('CREATE')
    print('LIST ====')
