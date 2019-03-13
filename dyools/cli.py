from __future__ import (absolute_import, division, print_function, unicode_literals)

import click
from past.types import basestring

from .klass_data import Data
from .klass_path import Path
from .klass_print import Print
from .klass_yaml_config import YamlConfig

CONFIG_FILE = Path.touch(Path.home(), '.dyvz', 'dyools.yml')


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
    DEFAULT = 'default'


DEFAULT_CONFIG = {
    ConfigEnum.HOST: 'localhost',
    ConfigEnum.PORT: 8069,
    ConfigEnum.DATABASE: 'demo',
    ConfigEnum.USER: 'admin',
    ConfigEnum.PASSWORD: 'admin',
    ConfigEnum.SUPERADMINPASSWORD: 'admin',
    ConfigEnum.PROTOCOL: 'jsonrpc',
    ConfigEnum.MODE: 'dev',
    ConfigEnum.DEFAULT: False,
}


def _check_production(ctx, config):
    if config.get(ConfigEnum.MODE, ConfigEnum.PRODUCTION) == ConfigEnum.PRODUCTION:
        click.confirm('Production environment, do you want to continue?', abort=True)


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
    configs = yaml_obj.get_data()
    ctx.obj = {}
    if load:
        if load not in configs:
            Print.error('The configuration [{}] not found!'.format(load))
        current_config = yaml_obj.get_values(name=load)
    else:
        current_config = yaml_obj.get_values(default=True) or DEFAULT_CONFIG
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
    ctx.obj['config_obj'] = yaml_obj
    ctx.obj['configs'] = configs
    ctx.obj['current_config'] = current_config


@cli.command('create')
@click.argument('name')
@click.pass_context
def __create_config(ctx, name):
    """Create a new configuration"""
    configs = ctx.obj['configs']
    current_config = ctx.obj['current_config']
    if name in configs:
        if not click.confirm('The name [{}] is already exists ! continue to update ?'.format(name)):
            ctx.abort()
    host = click.prompt(ConfigEnum.HOST, default=current_config[ConfigEnum.HOST], type=str)
    port = click.prompt(ConfigEnum.PORT, default=current_config[ConfigEnum.PORT], type=int)
    database = click.prompt(ConfigEnum.DATABASE, default=current_config[ConfigEnum.DATABASE], type=str)
    user = click.prompt(ConfigEnum.USER, default=current_config[ConfigEnum.USER], type=str)
    password = click.prompt(ConfigEnum.PASSWORD, default=current_config[ConfigEnum.PASSWORD], type=str)
    superadminpassword = click.prompt(ConfigEnum.SUPERADMINPASSWORD,
                                      default=current_config[ConfigEnum.SUPERADMINPASSWORD], type=str)
    protocol = click.prompt(ConfigEnum.PROTOCOL, default=current_config[ConfigEnum.PROTOCOL], type=str)
    mode = click.prompt(ConfigEnum.MODE, default=current_config[ConfigEnum.MODE], type=str)
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
    ctx.obj['config_obj'].switch(name, 'default', True, False)
    ctx.obj['config_obj'].dump()


def __list_configurations(ctx, filter=False, index=False):
    configs = ctx.obj['configs']
    data = Data(configs)
    tbl = data.get_pretty_table(add_index=True, filter=filter, index=index)
    Print.info(tbl, header="List of configurations", total=len(tbl._rows))


@cli.command('list')
@click.argument('filter', required=False)
@click.pass_context
def __list(ctx, filter):
    """List of configurations"""
    __list_configurations(ctx, filter)


@cli.command('use')
@click.argument('filter', required=False)
@click.pass_context
def __use(ctx, filter):
    """List of configurations"""
    configs = ctx.obj['configs']
    data = Data(configs)
    __list_configurations(ctx, filter)
    if not filter:
        filter = click.prompt('Enter the name or the index of a configuration to use')
    name = index = False
    for i, item in enumerate(data.get_lines(), 1):
        if filter:
            if isinstance(filter, basestring) and filter.strip().isdigit() and int(filter) == i:
                name = item[0]
                index = i
            if item[0] == filter:
                name = item[0]
                index = i
    if not name:
        Print.error('please retry with an other filter !')
    ctx.obj['config_obj'].switch(name, ConfigEnum.DEFAULT, True, False)
    ctx.obj['config_obj'].dump()
    __list_configurations(ctx, False, index=index)


@cli.command('delete')
@click.argument('filter', required=False)
@click.pass_context
def __delete(ctx, filter):
    """Delete a configuration"""
    configs = ctx.obj['configs']
    data = Data(configs)
    __list_configurations(ctx, filter)
    if not filter:
        filter = click.prompt('Enter the name or the index of a configuration to delete')
    name = index = False
    for i, item in enumerate(data.get_lines(), 1):
        if filter:
            if isinstance(filter, basestring) and filter.strip().isdigit() and int(filter) == i:
                name = item[0]
                index = i
            if item[0] == filter:
                name = item[0]
                index = i
    if not name:
        Print.error('please retry with an other filter !')
    click.confirm('Are you sure you want to delete the configuration [{}]'.format(name), abort=True)
    ctx.obj['config_obj'].delete(name=name)
    ctx.obj['config_obj'].dump()
    __list_configurations(ctx, False, index=index)
