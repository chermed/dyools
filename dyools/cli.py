from __future__ import (absolute_import, division, print_function, unicode_literals)

import sys

import click
from past.types import basestring

from .klass_data import Data
from .klass_odoo_rpc import RPC, CONFIG_FILE
from .klass_operator import Operator
from .klass_print import Print
from .klass_yaml_config import YamlConfig

ORDER = dict(id=1, display_name=2, name=2, key=3, user_id=4, partner_id=5, product_id=6)


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
    rpc = False
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
    if mode is not None:
        current_config[ConfigEnum.MODE] = mode

    def action_connect():
        global rpc
        if ConfigEnum.MODE == ConfigEnum.PRODUCTION:
            if not yes and not click.confirm('You are in mode production, continue ?'):
                sys.exit()
        try:
            Print.info('Try to connect to the host %s:%s, database=%s, mode=%s, timeout=%smin' % (
                current_config[ConfigEnum.HOST], current_config[ConfigEnum.PORT], current_config[ConfigEnum.DATABASE],
                current_config[ConfigEnum.MODE], timeout / 60))
            rpc = RPC(
                host=current_config[ConfigEnum.HOST],
                port=current_config[ConfigEnum.PORT],
                dbname=current_config[ConfigEnum.DATABASE],
                protocol=current_config[ConfigEnum.PROTOCOL],
                timeout=timeout)
            rpc.odoo.config['auto_context'] = not no_context
            Print.success(
                'Connected to host %s:%s, database=%s, version=%s, mode=%s, timeout=%smin' % (
                    current_config[ConfigEnum.HOST], current_config[ConfigEnum.PORT],
                    current_config[ConfigEnum.DATABASE], rpc.version, current_config[ConfigEnum.MODE], timeout / 60))
            ctx.obj['version'] = int(
                ''.join([x for x in rpc.version.strip() if x.isdigit() or x == '.']).split('.')[0])
        except:
            Print.error('Cannot connect to host %s:%s, database=%s, mode=%s' % (
                current_config[ConfigEnum.HOST], current_config[ConfigEnum.PORT], current_config[ConfigEnum.DATABASE],
                current_config[ConfigEnum.MODE]))
        return rpc

    def action_login():
        global rpc
        rpc = action_connect()
        if rpc:
            rpc = RPC(
                host=current_config[ConfigEnum.HOST],
                port=current_config[ConfigEnum.PORT],
                dbname=current_config[ConfigEnum.DATABASE],
                protocol=current_config[ConfigEnum.PROTOCOL],
                timeout=timeout)
            try:
                Print.info('Try to login to the database %s as %s' % (
                    current_config[ConfigEnum.DATABASE], current_config[ConfigEnum.USER]))
                rpc.login(
                    dbname=current_config[ConfigEnum.DATABASE],
                    user=current_config[ConfigEnum.USER],
                    password=current_config[ConfigEnum.PASSWORD])
                Print.success('Connected to the database %s as %s' % (
                    current_config[ConfigEnum.DATABASE], current_config[ConfigEnum.USER]))
            except:
                Print.error('Cannot connect to the database %s as %s' % (
                    current_config[ConfigEnum.DATABASE], current_config[ConfigEnum.USER]))
        return rpc

    def new_rpc():
        new_rpc = False
        if current_config[ConfigEnum.MODE] == ConfigEnum.PRODUCTION:
            if not yes and not click.confirm('You are in mode production, continue ?'):
                sys.exit()
        try:
            Print.info('Try to connect to the host %s:%s, database=%s, mode=%s, timeout=%smin' % (
                current_config[ConfigEnum.HOST], current_config[ConfigEnum.PORT], current_config[ConfigEnum.DATABASE],
                current_config[ConfigEnum.MODE], timeout / 60))
            new_rpc = RPC(
                host=current_config[ConfigEnum.HOST],
                port=current_config[ConfigEnum.PORT],
                dbname=current_config[ConfigEnum.DATABASE],
                protocol=current_config[ConfigEnum.PROTOCOL],
                timeout=timeout)
            new_rpc.config['auto_context'] = not no_context
            Print.success('Connected to host %s:%s, database=%s, version=%s, mode=%s, timeout=%smin' % (
                current_config[ConfigEnum.HOST], current_config[ConfigEnum.PORT], current_config[ConfigEnum.DATABASE],
                new_rpc.version, current_config[ConfigEnum.MODE], timeout / 60))
            ctx.obj['version'] = int(
                ''.join([x for x in new_rpc.version.strip() if x.isdigit() or x == '.']).split('.')[0])
            new_rpc = RPC(
                host=current_config[ConfigEnum.HOST],
                port=current_config[ConfigEnum.PORT],
                dbname=current_config[ConfigEnum.DATABASE],
                protocol=current_config[ConfigEnum.PROTOCOL],
                timeout=timeout)
            Print.info('Try to login to the database %s as %s' % (
                current_config[ConfigEnum.DATABASE], current_config[ConfigEnum.USER]))
            new_rpc.login(current_config[ConfigEnum.DATABASE], current_config[ConfigEnum.USER],
                          current_config[ConfigEnum.PASSWORD])
            Print.success('Connected to the database %s as %s' % (
                current_config[ConfigEnum.DATABASE], current_config[ConfigEnum.USER]))
        except:
            Print.error('Cannot connect to the database %s as %s' % (
                current_config[ConfigEnum.DATABASE], current_config[ConfigEnum.USER]))
        return new_rpc

    def update_list():
        global odoo
        if odoo:
            Print.info('Updating the list of modules ...')
            odoo.env['ir.module.module'].update_list()

    ctx.obj['config_obj'] = yaml_obj
    ctx.obj['configs'] = configs
    ctx.obj['current_config'] = current_config
    ctx.obj['action_connect'] = action_connect
    ctx.obj['action_login'] = action_login
    ctx.obj['update_list'] = update_list
    ctx.obj['new_rpc'] = new_rpc
    ctx.obj['rpc'] = rpc


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


def __list_configurations(ctx, grep=False, index=False):
    configs = ctx.obj['configs']
    data = Data(configs)
    tbl = data.get_pretty_table(add_index=True, grep=grep, index=index)
    Print.info(tbl, header="List of configurations", total=len(tbl._rows))


@cli.command('list')
@click.argument('grep', required=False)
@click.pass_context
def __list(ctx, grep):
    """List of configurations"""
    __list_configurations(ctx, grep)


@cli.command('use')
@click.argument('grep', required=False)
@click.pass_context
def __use(ctx, grep):
    """List of configurations"""
    configs = ctx.obj['configs']
    data = Data(configs)
    __list_configurations(ctx, grep)
    if not grep:
        grep = click.prompt('Enter the name or the index of a configuration to use')
    name = index = False
    for i, item in enumerate(data.get_lines(), 1):
        if grep:
            if isinstance(grep, basestring) and grep.strip().isdigit() and int(grep) == i:
                name = item[0]
                index = i
            if item[0] == grep:
                name = item[0]
                index = i
    if not name:
        Print.error('please retry with an other grep !')
    ctx.obj['config_obj'].switch(name, ConfigEnum.DEFAULT, True, False)
    ctx.obj['config_obj'].dump()
    __list_configurations(ctx, False, index=index)


@cli.command('delete')
@click.argument('grep', required=False)
@click.pass_context
def __delete(ctx, grep):
    """Delete a configuration"""
    configs = ctx.obj['configs']
    data = Data(configs)
    __list_configurations(ctx, grep)
    if not grep:
        grep = click.prompt('Enter the name or the index of a configuration to delete')
    name = index = False
    for i, item in enumerate(data.get_lines(), 1):
        if grep:
            if isinstance(grep, basestring) and grep.strip().isdigit() and int(grep) == i:
                name = item[0]
                index = i
            if item[0] == grep:
                name = item[0]
                index = i
    if not name:
        Print.error('please retry with an other grep !')
    click.confirm('Are you sure you want to delete the configuration [{}]'.format(name), abort=True)
    ctx.obj['config_obj'].delete(name=name)
    ctx.obj['config_obj'].dump()
    __list_configurations(ctx, False, index=index)


@cli.command('login')
@click.argument('user', required=False)
@click.argument('password', required=False)
@click.pass_context
def __login(ctx, user, password):
    """Login to the database"""
    if user:
        ctx.obj['current_config'].update(dict(user=user))
    if password:
        ctx.obj['current_config'].update(dict(password=password))
    ctx.obj['action_login']()


@cli.command('connect')
@click.argument('host', required=False)
@click.argument('port', required=False)
@click.pass_context
def __connect(ctx, host, port):
    """Connect to the server"""
    if host:
        ctx.obj['current_config'].update(dict(host=host))
    if port:
        ctx.obj['current_config'].update(dict(port=port))
    ctx.obj['action_connect']()


@cli.command('param')
@click.argument('key', default=None, required=False)
@click.argument('value', default=None, required=False)
@click.pass_context
def __params(ctx, key, value):
    """Manage parameters"""
    rpc = ctx.obj['action_login']()
    fields = ['id', 'key', 'value']
    domain = []
    result = None
    if key:
        result = rpc.get_param(key)
    if value is not None:
        result = rpc.set_param(key, value)
    if result is None:
        data = Data(rpc.read('ir.config_parameter', domain=domain, fields=fields), header=fields)
        Print.info(data.get_pretty_table())
    else:
        Print.info('[{} => {}]'.format(key, result))


@cli.command('data')
@click.argument('model', default=None, required=True)
@click.option('domain', '-d', type=click.STRING, default='', help="Domain")
@click.option('limit', '-l', type=click.INT, default=0, help="Limit")
@click.option('order', '-o', type=click.STRING, default='', help="Order")
@click.option('fields', '-f', multiple=True, type=click.STRING, default='', help="Fields to show")
@click.pass_context
def __data(ctx, model, domain, limit, order, fields):
    """Show the data"""
    fields = Operator.split_and_flat(',', fields) if fields else ['id', 'name']
    rpc = ctx.obj['action_login']()
    kwargs = dict(domain=domain, fields=fields)
    if limit: kwargs.update(dict(limit=limit))
    if order: kwargs.update(dict(order=order))
    Data(rpc.read(model, **kwargs), header=fields).show()


@cli.command('fields')
@click.argument('model', default=None, required=True)
@click.option('fields', '-f', multiple=True, type=click.STRING, default='', help="Fields to show")
@click.option('grep', '-g', type=click.STRING, default=False, help="Grep the result")
@click.pass_context
def __fields(ctx, model, fields, grep):
    """Fields of a model"""
    rpc = ctx.obj['action_login']()
    fields = ['name', 'type'] + Operator.split_and_flat(',', fields)
    Data(rpc.env[model].fields_get(), header=fields, name='name').show(grep=grep)
