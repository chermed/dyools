from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
from os.path import expanduser

import click

from .klass_data import Data
from .klass_print import Print
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


class ConfigEnum(object):
    HOST = 'host'
    PORT = 'port'
    DATABASE = 'database'
    USER = 'user'
    PASSWORD = 'password'
    SUPERADMINPASSWORD = 'superadminpassword'
    PROTOCOL = 'protocol'
    MODE = 'mode'
    PRODUCTION = 'production'
    TEST = 'test'
    DEVELOPPEMENT = 'developpement'
    MODES = [PRODUCTION, TEST, DEVELOPPEMENT]
    PROTOCOLS = ['jsonrpc', 'jsonrpc+ssl']


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
@click.option('--protocol', type=click.Choice(ConfigEnum.PROTOCOLS), default=None, help="Protocol")
@click.option('--mode', '-m', type=click.Choice(ConfigEnum.MODES), default=None, help="Mode")
@click.option('--timeout', '-t', type=click.INT, default=60, help="Timeout in minutes")
@click.option('--yes', is_flag=True, default=False)
@click.option('--no-context', is_flag=True, default=False)
@click.option('--debug', is_flag=True, default=False)
@click.option('--workers', '-w', type=click.INT, default=0)
@click.pass_context
def cli(ctx, database, host, port, user, password, superadminpassword, protocol, timeout, config, load, mode,
        prompt_login, prompt_connect, yes, no_context, debug, workers):
    yaml_obj = YamlConfig(config)
    current_config = yaml_obj.get(default=True) or DEFAULT_CONFIG
    configs = yaml_obj.get_data() or DEFAULT_CONFIG
    ctx.obj = {}
    ctx.obj['config_obj'] = yaml_obj
    ctx.obj['configs'] = configs
    ctx.obj['current_config'] = current_config
    if load:
        if load not in configs:
            Print.error('The configuration [{}] not found!'.format(load))
        current_config = yaml_obj.get(name=load)
    else:
        current_config = yaml_obj.get(default=True) or DEFAULT_CONFIG
    if host is not None:
        current_config[ConfigEnum.HOST] = host
    if port is not None:
        current_config[ConfigEnum.PORT] = port
    if database is not None:
        current_config[ConfigEnum.DATABASE] = database
    if user is not None:
        current_config[ConfigEnum.USER] = user
    if password is not None:
        current_config[ConfigEnum.PASSWORD] = password
    if superadminpassword is not None:
        current_config[ConfigEnum.SUPERADMINPASSWORD] = superadminpassword
    if protocol is not None:
        current_config[ConfigEnum.PROTOCOL] = protocol
    if current_config.get(ConfigEnum.MODE, ConfigEnum.PRODUCTION) == ConfigEnum.PRODUCTION:
        click.confirm('Production environnement, do you want to continue?', abort=True)


@cli.command('create')
@click.argument('name')
@click.pass_context
def __create_config(ctx, name):
    """Create a new configuration"""
    configs = ctx.obj['configs']
    if name in configs:
        Print.error('The name [{}] is already exists !'.format(name))
    host = click.prompt(ConfigEnum.HOST, default=DEFAULT_CONFIG[ConfigEnum.HOST], type=str)
    port = click.prompt(ConfigEnum.PORT, default=DEFAULT_CONFIG[ConfigEnum.PORT], type=int)
    database = click.prompt(ConfigEnum.DATABASE, default=DEFAULT_CONFIG[ConfigEnum.DATABASE], type=str)
    user = click.prompt(ConfigEnum.USER, default=DEFAULT_CONFIG[ConfigEnum.USER], type=str)
    password = click.prompt(ConfigEnum.PASSWORD, default=DEFAULT_CONFIG[ConfigEnum.PASSWORD], type=str)
    superadminpassword = click.prompt(ConfigEnum.SUPERADMINPASSWORD,
                                      default=DEFAULT_CONFIG[ConfigEnum.SUPERADMINPASSWORD], type=str)
    protocol = click.prompt(ConfigEnum.PROTOCOL, default=DEFAULT_CONFIG[ConfigEnum.PROTOCOL], type=str)
    mode = click.prompt(ConfigEnum.MODE, default=DEFAULT_CONFIG[ConfigEnum.MODE], type=str)
    data = DEFAULT_CONFIG.copy()
    data.update(dict(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
        superadminpassword=superadminpassword,
        protocol=protocol,
        mode=mode))
    ctx.obj['config_obj'].add(name, **data)
    ctx.obj['config_obj'].dump()


@cli.command('list')
@click.pass_context
def __list(ctx):
    """List of configurations"""
    configs = ctx.obj['configs']
    data = Data(configs)
    len_tbl = len(configs)
    tbl = data.get_pretty_table()
    Print.info(tbl, header="List of configurations", total=len_tbl)
