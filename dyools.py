#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

import base64
import calendar
import importlib
import inspect
import logging
import os
import re
import shutil
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, date
from pprint import pprint

import click
import odoorpc
import yaml
from dateutil.parser import parse as dtparse
from dateutil.relativedelta import relativedelta

try:
    basestring
except NameError:
    basestring = str

try:
    from odoo.tools import human_size
except:
    human_size = lambda r: r

__VERSION__ = '0.8.0'
__AUTHOR__ = ''
__WEBSITE__ = ''
__DATE__ = ''

DATE_FORMAT, DATETIME_FORMAT = "%Y-%m-%d", "%Y-%m-%d %H:%M:%S"
DATE_FR_FORMAT, DATETIME_FR_FORMAT = "%d/%m/%Y", "%d/%m/%Y %H:%M:%S"
DATE_TYPE, DATETIME_TYPE = "date", "datetime"

logger = logging.getLogger(__name__)


def signature(callable):
    if getattr(inspect, 'signature'):
        pprint(inspect.signature(callable))
    if getattr(inspect, 'getargspec'):
        pprint(inspect.getargspec(callable))
    if getattr(inspect, 'getfullargspec'):
        pprint(inspect.getfullargspec(callable))


def date_range(dt_start, dt_stop=False, **kwargs):
    dt = Date(dt_start)
    stop = dt_stop
    if stop:
        dt_stop = Date(dt_stop)
    if not kwargs:
        kwargs = {'days': 1}
    while True:
        yield dt.to_str()
        dt = dt.apply(**kwargs)
        if stop and dt_stop.to_str() < dt.to_str():
            break


class Date(object):
    def __init__(self, *args, **kwargs):
        assert args or kwargs, "arguments should be a date or parameters for datetime"
        ttype = dt = False
        if len(args) == 1:
            item = args[0]
            if isinstance(item, basestring):
                if len(item) == 10:
                    dt = datetime.strptime(item, DATE_FORMAT)
                    ttype = DATE_TYPE
                elif len(item) == 19:
                    dt = datetime.strptime(item, DATETIME_FORMAT)
                    ttype = DATETIME_TYPE
                else:
                    dt = dtparse(item)
                    if ':' in item:
                        ttype = DATETIME_TYPE
                    else:
                        ttype = DATE_TYPE
            elif isinstance(item, datetime):
                dt = item
                ttype = DATETIME_TYPE
            elif isinstance(item, date):
                dt = datetime(item.year, item.month, item.day)
                ttype = DATE_TYPE
            elif isinstance(item, Date):
                dt = item.dt
                ttype = item.ttype
        else:
            dt = datetime(*args, **kwargs)
            if len(args) + len(kwargs) == 3:
                ttype = DATE_TYPE
            else:
                ttype = DATETIME_FORMAT
        assert ttype and dt, "The format of date [%s] is not valid" % item
        self.dt = dt
        self.ttype = ttype

    def relativedelta(self, **kwargs):
        self.apply(**kwargs)
        if self.ttype == DATE_TYPE:
            return self.dt.strftime(DATE_FORMAT)
        else:
            return self.dt.strftime(DATETIME_FORMAT)

    def apply(self, **kwargs):
        sub = kwargs.get('sub', False) == True
        if 'sub' in kwargs: del kwargs['sub']
        if sub:
            self.dt = self.dt - relativedelta(**kwargs)
        else:
            self.dt = self.dt + relativedelta(**kwargs)
        return self

    def first_day(self):
        dt = self.dt + relativedelta(day=1)
        if self.ttype == DATE_TYPE:
            return dt.strftime(DATE_FORMAT)
        else:
            return dt.strftime(DATETIME_FORMAT)

    def last_day(self):
        dt = self.dt + relativedelta(day=calendar.monthrange(self.dt.year, self.dt.month)[1])
        if self.ttype == DATE_TYPE:
            return dt.strftime(DATE_FORMAT)
        else:
            return dt.strftime(DATETIME_FORMAT)

    def to_datetime(self):
        return self.dt

    def to_date(self):
        return self.dt.date()

    def to_str(self):
        if self.ttype == DATE_TYPE:
            return self.dt.strftime(DATE_FORMAT)
        else:
            return self.dt.strftime(DATETIME_FORMAT)

    def to_fr(self):
        if self.ttype == DATE_TYPE:
            return self.dt.strftime(DATE_FR_FORMAT)
        else:
            return self.dt.strftime(DATETIME_FR_FORMAT)

    def is_between(self, dt_start, dt_stop):
        dt_start = Date(dt_start) if dt_start else False
        dt_stop = Date(dt_stop) if dt_stop else False
        dt = self
        if dt_start and dt_stop:
            if dt_stop < dt_start:
                dt_start, dt_stop = dt_stop, dt_start
            return dt >= dt_start and dt <= dt_stop
        elif dt_start:
            return dt >= dt_start
        elif dt_stop:
            return dt <= dt_stop
        else:
            return True

    def _apply_add_sub(self, other, sub=False):
        kwargs = {}
        mapping = {
            'y': 'years',
            'm': 'months',
            'd': 'days',
            'H': 'hours',
            'M': 'minutes',
            'S': 'seconds',
        }
        assert isinstance(other, (basestring, int)), "format of [%s] is invalid" % other
        if isinstance(other, basestring):
            coef = 1
            if other and other[0] in ['+', '-']:
                coef, other = other[0], other[1:]
                coef = -1 if coef == '-' else 1
            assert len(other) > 1 and other[-1] in mapping.keys(), "format of [%s] is invalid" % other
            assert other[:-1].isdigit(), "format of [%s] is invalid" % other
            kwargs[mapping[other[-1]]] = coef * int(other[:-1])
        elif isinstance(other, int):
            kwargs['days'] = other
        if sub: kwargs['sub'] = True
        return self.relativedelta(**kwargs)

    def __sub__(self, other):
        return self._apply_add_sub(other, sub=True)

    def __add__(self, other):
        return self._apply_add_sub(other)

    def __str__(self):
        if self.ttype == DATE_TYPE:
            return self.dt.strftime(DATE_FORMAT)
        else:
            return self.dt.strftime(DATETIME_FORMAT)

    def __repr__(self):
        if self.ttype == DATE_TYPE:
            return self.dt.strftime(DATE_FORMAT)
        else:
            return self.dt.strftime(DATETIME_FORMAT)

    def __lt__(self, other):
        return self.to_str() < Date(other).to_str()

    def __le__(self, other):
        return self.to_str() <= Date(other).to_str()

    def __eq__(self, other):
        return self.to_str() == Date(other).to_str()

    def __ne__(self, other):
        return self.to_str() != Date(other).to_str()

    def __gt__(self, other):
        return self.to_str() > Date(other).to_str()

    def __ge__(self, other):
        return self.to_str() >= Date(other).to_str()


def create_file(path, content):
    def _erase_data(_path, _content):
        with open(_path, 'w+') as f:
            f.write(_content)

    if not os.path.isfile(path):
        ddir = os.path.dirname(path)
        create_dir(ddir)
        _erase_data(path, content)
    else:
        with open(path, 'r') as f:
            c = f.read()
        if c != content:
            _erase_data(path, content)


def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def clean_dir(path):
    if os.path.exists(path):
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            elif os.path.isfile(full_path):
                os.remove(full_path)


def delete_path(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def contruct_domain_from_str(domain):
    AND, OR = ' and ', ' or '
    assert '(' not in domain, "can not process parenthese in string domain"
    if AND in domain:
        assert OR not in domain, "domain should not have or and and operators"
    if OR in domain:
        assert AND not in domain, "domain should not have or and and operators"
    and_or = '|' if OR in domain else '&'
    tuples = []
    tuples1 = domain.split(AND)
    [tuples.extend(t.split(OR)) for t in tuples1 if t]
    domain = [tuple(t.split()) for t in tuples if t]
    if not domain:
        res = []
    else:
        for ttuple in domain:
            assert len(ttuple) == 3, 'a condition should have 3 parts [%s]' % ttuple
        i = 0
        for key, op, value in domain:
            float_parts = value.split('.')
            isfloat = len(float_parts) == 2
            if op == "==": op = '='
            if value == 'False':
                value = False
            elif value == 'True':
                value = True
            elif value.isdigit():
                value = int(value)
            elif isfloat and float_parts[0].isdigit() and float_parts[1].isdigit():
                value = float(value)
            domain[i] = (key, op, value)
            i += 1
        if len(domain) > 1:
            domain = [and_or] * (len(domain) - 1) + domain
        res = domain
    return res


class Mixin(object):
    def __init__(self):
        pass

    def _require_env(self):
        assert self.env, "An environment is required for this method"

    def info(self, *args, **kwargs):
        logger.info(*args, **kwargs)

    def debug(self, *args, **kwargs):
        logger.debug(*args, **kwargs)

    def warning(self, *args, **kwargs):
        logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        logger.error(*args, **kwargs)

    def get_param(self, param, default=False):
        self._require_env()
        return self.env['ir.config_parameter'].get_param(param, default)

    def set_param(self, param, value):
        self._require_env()
        self.env['ir.config_parameter'].set_param(param, value)
        return self.get_param(param)

    def show(self, records, fields=[], types=[], title=False):
        self._require_env()
        if isinstance(types, basestring):
            types = types.split()
        if isinstance(fields, basestring):
            fields = fields.split()
        assert isinstance(fields, list), 'fields should be a list'
        if title:
            print('@@@@ %s @@@@' % title)
        print('Show %s record(s)' % len(records))
        if not fields:
            if isinstance(records, odoorpc.env.Model):
                fields = list(self.env[records._name].fields_get().keys())
            else:
                fields = list(records.fields_get().keys())
        if types:
            if isinstance(records, odoorpc.env.Model):
                fields_get = self.env[records._name].fields_get()
            else:
                fields_get = records.fields_get()
            fields = filter(lambda f: '.' not in f and fields_get[f]['type'] in types, fields)
            fields = [f for f in fields]
        if not fields:
            print('Not field is given')
            return False
        for record in records:
            print('%s Record [ID=%s][Name=%s]' % ('#' * 40, record.id, getattr(record, 'display_name', '')))
            for field in fields:
                print("{:_<40}<{}>".format(field, record.mapped(field) if '.' in field else record[field]))

    def path(self, module):
        if isinstance(module, basestring):
            module = importlib.import_module(module)
        return os.path.dirname(module.__file__)

    def get(self, model, domain=[], limit=False, order=False):
        self._require_env()
        records = model
        if isinstance(domain, int):
            domain = [('id', '=', domain)]
        elif isinstance(domain, tuple):
            domain = [domain]
        if isinstance(domain, basestring):
            domain = contruct_domain_from_str(domain)
        if hasattr(self.odoo, 'models') and isinstance(records, self.odoo.models.Model):
            domain = ['&', ('id', 'in', records.ids)] + domain
            model = records._name
        if isinstance(records, odoorpc.env.Model):
            domain = ['&', ('id', 'in', records.ids)] + domain
            model = records._name
        kwargs = {}
        if limit: kwargs['limit'] = limit
        if order: kwargs['order'] = order
        res = self.env[model].search(domain, **kwargs)
        res = self.obj(model, res)
        return res

    def get_users(self, domain=[], limit=False, order=False):
        self._require_env()
        return self.get('res.users', domain, limit, order)

    def get_partners(self, domain=[], limit=False, order=False):
        self._require_env()
        return self.get('res.partner', domain, limit, order)

    def get_products(self, domain=[], limit=False, order=False):
        self._require_env()
        return self.get('product.product', domain, limit, order)

    def get_templates(self, domain=[], limit=False, order=False):
        self._require_env()
        return self.get('product.template', domain, limit, order)

    def get_invoices(self, domain=[], limit=False, order=False):
        self._require_env()
        return self.get('account.invoice', domain, limit, order)

    def get_sales(self, domain=[], limit=False, order=False):
        self._require_env()
        return self.get('sale.order', domain, limit, order)

    def get_purchases(self, domain=[], limit=False, order=False):
        self._require_env()
        return self.get('sale.purchase', domain, limit, order)

    def get_locations(self, domain=[], limit=False, order=False):
        self._require_env()
        return self.get('stock.location', domain, limit, order)

    def get_quants(self, domain=[], limit=False, order=False):
        self._require_env()
        return self.get('stock.quant', domain, limit, order)

    def get_pickings(self, domain=[], limit=False, order=False):
        self._require_env()
        return self.get('stock.picking', domain, limit, order)

    def get_stock_moves(self, domain=[], limit=False, order=False):
        self._require_env()
        return self.get('stock.move', domain, limit, order)

    def get_account_moves(self, domain=[], limit=False, order=False):
        self._require_env()
        return self.get('account.move', domain, limit, order)

    def get_account_move_liness(self, domain=[], limit=False, order=False):
        self._require_env()
        return self.get('account.move.line', domain, limit, order)

    def get_aml(self, domain=[], limit=False, order=False):
        self._require_env()
        return self.get('account.move.line', domain, limit, order)

    def update_xmlid(self, record, xmlid=False):
        self._require_env()
        assert not xmlid or len(xmlid.split('.')) == 2, "xmlid [%s] is invalid" % xmlid
        xmlid_env = self.env['ir.model.data']
        xmlid_obj = xmlid_env.search([('model', '=', record._name), ('res_id', '=', record.id)], limit=1)
        if not xmlid_obj:
            if xmlid:
                module, name = xmlid.split('.')
            else:
                module = '__export__'
                name = '%s_%s' % (record._name.replace('.', '_'), record.id)
            xmlid_obj = xmlid_env.create({
                'module': module,
                'name': name,
                'model': record._name,
                'res_id': record.id,
            })
        if isinstance(xmlid_obj, (int, list)):
            xmlid_obj = xmlid_env.browse(xmlid_obj)
        return xmlid_obj.complete_name

    def obj(self, model, res):
        if isinstance(res, (int, list)):
            return self.env[model].browse(res)
        return res

    def _process_addons_op(self, addons, op):
        self._require_env()
        if isinstance(addons, basestring):
            addons = addons.split()
        addons = self.env['ir.module.module'].search([('name', 'in', addons)])
        addons = self.obj('ir.module.module', addons)
        addons_names = addons.mapped('name')
        self.show(addons, fields=['name', 'state'], title="modules before")
        addons = self.env['ir.module.module'].search([('name', 'in', addons_names)])
        addons = self.obj('ir.module.module', addons)
        assert op in ['install', 'upgrade', 'uninstall'], "opeartion %s is npt mapped" % op
        if op == 'install':
            addons.button_immediate_install()
        elif op == 'upgrade':
            addons.button_immediate_upgrade()
        elif op == 'uninstall':
            addons.module_uninstall()
        self.show(addons, fields=['name', 'state'], title="modules after")

    def install(self, addons):
        self._process_addons_op(addons, 'install')

    def upgrade(self, addons):
        self._process_addons_op(addons, 'upgrade')

    def uninstall(self, addons):
        self._process_addons_op(addons, 'uninstall')


class RPC(Mixin):
    def __init__(self, *args, **kwargs):
        items = ['host', 'port', 'dbname', 'user', 'password', 'superadminpassword', 'protocol', 'ssl']
        for i, arg in enumerate(args):
            kwargs[items[i]] = arg
        host = kwargs.get('host', os.environ.get('RPC_HOST'))
        port = kwargs.get('port', os.environ.get('RPC_PORT'))
        dbname = kwargs.get('dbname', os.environ.get('RPC_DBNAME'))
        user = kwargs.get('user', os.environ.get('RPC_USER'))
        password = kwargs.get('password', os.environ.get('RPC_PASSWORD'))
        superadminpassword = kwargs.get('superadminpassword', os.environ.get('RPC_SUPERADMINPASSWORD'))
        protocol = kwargs.get('protocol', os.environ.get('RPC_PROTOCOL'))
        timeout = kwargs.get('timeout', os.environ.get('RPC_TIMEOUT'))
        timeout = int(timeout) if timeout else 120
        if not protocol:
            if kwargs.get('ssl', False) == True:
                protocol = 'jsonrpc+ssl'
            else:
                protocol = 'jsonrpc'
        assert host and port and dbname, "please provide host, port and dbname"
        port = int(port)
        self.dbname = dbname
        odoo = odoorpc.ODOO(host=host, protocol=protocol, port=port, timeout=timeout)
        self.env = False
        self.odoo = odoo
        self.superadminpassword = superadminpassword
        self.user = user
        self.password = password

    def login(self):
        assert self.user and self.password, "please provide the user and the password"
        self.odoo.login(self.dbname, self.user, self.password)
        self.env = self.odoo.env
        return self.env

    def timeout(self, timeout):
        self.odoo.config['timeout'] = timeout
        return self.odoo.config['timeout']

    def dump_db(self, dest, zip=True):
        try:
            os.makedirs(dest)
        except:
            pass
        assert os.path.isdir(dest), "The directory [%s] should exists" % dest
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        ext = 'zip' if zip else 'dump'
        filename = "{}_{}.{}".format(self.dbname, now, ext)
        path = os.path.join(dest, filename)
        with open(path, 'wb+') as destination:
            kwargs = {}
            if not zip: kwargs['backup_format'] = 'custom'
            dump = self.odoo.db.dump(self.superadminpassword, self.dbname)
            with open(path, 'wb') as dump_zip:
                dump_zip.write(dump.read())
        pprint('End: %s' % path)
        size = human_size(os.path.getsize(path))
        pprint('Size: %s' % size)
        return path

    def drop_db(self):
        try:
            self.odoo.db.drop(self.superadminpassword, self.dbname)
        except Exception as e:
            pass
        pprint('End: dbname=%s is dropped' % self.dbname)
        return self.dbname

    def restore_db(self, path, drop=False):
        assert os.path.isfile(path), 'The path [%s] sould be a file' % path
        if drop:
            self.drop_db()
        size = human_size(os.path.getsize(path))
        pprint('Size: %s' % size)
        with open(path, 'rb') as dump_zip:
            self.odoo.db.restore(self.superadminpassword, self.dbname, dump_zip)
        pprint('End: %s dbname=%s' % (path, self.dbname))
        return path


class Env(Mixin):
    def __init__(self, env=False, odoo=False, dbname=False, verbose=True):
        assert (env and odoo) or (
                odoo and dbname), "give an existing environnement or specify odoo and dbname for creating a new one"
        self.odoo = odoo
        self.dbname = dbname
        self.verbose = verbose
        self.cr = False
        self.conf = self.odoo.tools.config
        self.list_db = self.odoo.tools.config['list_db']
        self.list_db_disabled = self.odoo.tools.config['list_db'] == False
        self.version = odoo.release.version_info[0]
        if env:
            self.env = env
            self.dbname = self.env.cr.dbname
            self.cr = self.env.cr
        else:
            self.reset()

    def reset(self):
        if self.cr and not self.cr.closed:
            print('closing the cursor')
            self.cr.close()
        try:
            registry = self.odoo.modules.registry.Registry.new(self.dbname)
            cr = registry.cursor()
            self.env = self.odoo.api.Environment(cr, self.odoo.SUPERUSER_ID, {})
        except Exception as e:
            self.env = False
        if self.env:
            self.dbname = self.env.cr.dbname
            self.cr = self.env.cr
        else:
            self.cr = False

    def close(self):
        self._require_env()
        if not self.cr.closed:
            self.cr.close()

    def get_addons(self, enterprise=False, core=False, extra=True, addons_path=False):
        self._require_env()
        installed, uninstalled = [], []
        addons_path = addons_path or self.conf['addons_path'].split(',')
        for path in addons_path:
            dirs = [ddir for ddir in os.listdir(path) if os.path.isdir(os.path.join(path, ddir))]
            addons = [ddir for ddir in dirs if
                      len({'__manifest__.py', '__init__.py'} & set(os.listdir(os.path.join(path, ddir)))) == 2]
            modules = self.env['ir.module.module'].search([('name', 'in', addons)])
            addons = modules.mapped('name')
            if not addons:
                continue
            if not core and {'base', 'sale', 'account'} & set(addons):
                continue
            if not enterprise and {'account_reports'} & set(addons):
                continue
            if not extra and not ({'base', 'sale', 'account_reports'} & set(addons)):
                continue
            installed.extend(modules.filtered(lambda a: a.state == 'installed').mapped('name'))
            uninstalled.extend(modules.filtered(lambda a: a.state == 'uninstalled').mapped('name'))
        return installed, uninstalled

    def check_uninstalled_modules(self, enterprise=False, core=False, extra=True, addons_path=False):
        self._require_env()
        installed, uninstalled = self.get_addons(enterprise=enterprise, core=core, extra=extra, addons_path=addons_path)
        pprint('Installed modules   : %s' % installed)
        pprint('Uninstalled modules : %s' % uninstalled)
        if uninstalled:
            sys.exit(-1)
        else:
            sys.exit(0)

    def _process_python(self, script, context, assets):
        res = exec(script, context)
        if isinstance(res, dict):
            context.update(res)

    def _normalize_value_for_field(self, model, field, value, assets):
        values = {}
        ffield = self.env[model].fields_get()[field]
        ttype, relation, selection = ffield['type'], ffield.get('relation'), ffield.get('selection', [])
        if ttype == 'boolean':
            value = bool(value)
        elif ttype in ['text', 'float', 'char', 'integer', 'monetary', 'html']:
            pass
        elif ttype == 'date':
            if isinstance(value, date):
                value = value.strftime(DATE_FORMAT)
            else:
                value = dtparse(str(value), dayfirst=True, fuzzy=True).strftime(DATE_FORMAT)
        elif ttype == 'datetime':
            if isinstance(value, datetime):
                value = value.strftime(DATETIME_FORMAT)
            else:
                value = dtparse(str(value), dayfirst=True, fuzzy=True).strftime(DATETIME_FORMAT)
        elif ttype == 'selection':
            for k, v in selection:
                if k == value or v == value:
                    value = k
                    break
        if ttype == 'binary':
            if assets:
                value = os.path.join(assets, value)
            with open(value, "rb") as binary_file:
                value = base64.b64encode(binary_file.read())
        if ttype in ['many2one', 'many2many', 'one2many']:
            ids = None
            if value == '__all__':
                ids = self.env[relation].search([]).ids
            elif value == '__first__':
                ids = self.env[relation].search([], limit=1, order="id asc").ids
            elif value == '__last__':
                ids = self.env[relation].search([], limit=1, order="id desc").ids
            elif isinstance(value, list) and IF.is_domain(value):
                ids = self.env[relation].search(value).ids
            elif isinstance(value, int):
                ids = [value]
            elif isinstance(value, basestring):
                if IF.is_xmlid(value):
                    ids = self.env.ref(value).ids
                else:
                    ids = self.env[relation].search([('name', '=', value)]).ids
            if ttype == 'many2one':
                value = value if not ids else ids[0]
            elif ttype == 'many2many':
                value = value if ids is None else [(6, 0, ids)]
        values[field] = value
        return values

    def _normalize_record_data(self, model, data, context, assets):
        record_data = {}
        model_env = self.env[model]
        onchange_specs = model_env._onchange_spec()
        for item in data:
            item = Eval(item, context).eval()
            for field, value in item.items():
                values = self._normalize_value_for_field(model, field, value, assets)
                record_data.update(values)
                onchange_values = model_env.onchange(record_data, field, onchange_specs)
                for k, v in onchange_values.get('value', {}).items():
                    if isinstance(v, (list, tuple)) and len(v) == 2:
                        v = v[0]
                    record_data[k] = v
        return record_data

    def _process_record(self, data, context, assets):
        records = self.env[data['model']]
        refs = data.get('refs')
        record_data = data.get('data')
        record_functions = data.get('functions', [])
        record_export = data.get('export')
        record_filter = data.get('filter')
        record_ctx = data.get('context', {})
        if context.get('__global_context__'):
            record_ctx.update(context.get('__global_context__'))
        if refs:
            if isinstance(refs, int):
                records = records.browse(refs)
            elif IF.is_xmlid(refs):
                records = records.env.ref(refs, raise_if_not_found=False) or records
            elif isinstance(refs, basestring):
                records = records.search([('name', '=', refs)])
            elif isinstance(refs, list):
                refs = Eval(refs, context).eval()
                records = records.search(refs)
            records = records.exists()
            if record_filter:
                if len(records) > 0:
                    print(['&', ('id', 'in', records.ids)] + record_filter)
                    records = records.search(['&', ('id', 'in', records.ids)] + record_filter)
                    if not records:
                        return False
        if record_ctx:
            records = records.with_context(**record_ctx)
        if record_data:
            assert isinstance(record_data, list), "The data [%s] should be a list" % record_data
            record_data = self._normalize_record_data(records._name, record_data, context, assets)
            if len(records) > 0:
                records.write(record_data)
            else:
                records = records.create(record_data)
                if isinstance(refs, basestring) and IF.is_xmlid(refs):
                    self.update_xmlid(records, xmlid=refs)
        if record_export:
            context[record_export] = records
        context['%s_record' % records._name.replace('.', '_')] = records
        for function in record_functions:
            func_name = function['name']
            func_args = function['args'] if function.get('args') else []
            func_kwargs = function['kwargs'] if function.get('kwargs') else {}
            assert isinstance(func_args, list), "Args [%s] should be a list" % func_args
            assert isinstance(func_kwargs, dict), "Kwargs [%s] should be a dict" % func_kwargs
            func_res = getattr(records, func_name)(*func_args, **func_kwargs)
            func_export = function.get('export')
            if func_export:
                context[func_export] = func_res
            context['%s_%s' % (records._name.replace('.', '_'), func_name)] = func_res

    def _process_yaml_doc(self, index, doc, context, assets):
        for key, value in doc.items():
            if key == 'python':
                print("[%s] ***** Execute python *****" % index)
                self._process_python(value, context, assets)
            elif key == 'record':
                print("[%s] ***** Process record *****" % index)
                self._process_record(value, context, assets)
            elif key == 'title':
                value = Eval(value, context).eval()
                print("[%s] ***** %s *****" % (index, value))
            elif key == 'context':
                value = Eval(value, context).eval()
                context['__global_context__'].update(value)
                print("[%s] ***** Add global context *****" % index)
            elif key == 'install':
                print("[%s] ***** Install modules *****" % index)
                self.install(value)
            elif key == 'upgrade':
                print("[%s] ***** Upgrade modules *****" % index)
                self.upgrade(value)
            elif key == 'uninstall':
                print("[%s] ***** Uninstall modules *****" % index)
                self.uninstall(value)

    def load_yaml(self, path, assets=False, start=False, stop=False, auto_commit=False):
        def __add_file(f):
            fname, ext = os.path.splitext(f)
            if ext.strip().lower() not in ['.yaml', '.yml']:
                return
            fname = os.path.basename(fname)
            idx = False
            try:
                idx = int(fname.split('-')[0].strip())
            except:
                pass
            if idx and (start or stop):
                if start and idx < start: return
                if stop and idx > stop: return
            files.append(f)

        self._require_env()
        assert not assets or os.path.exists(assets), "The path [%s] should exists" % assets
        files = []
        if isinstance(path, basestring):
            paths = [path]
        else:
            paths = path
            for path in paths:
                assert os.path.exists(path), "The path [%s] sould exists" % path
        for path in paths:
            if os.path.isdir(path):
                for dirpath, _, filenames in os.walk(path):
                    for filename in filenames:
                        __add_file(os.path.join(dirpath, filename))
            elif os.path.isfile(path):
                __add_file(path)
        print('[%s] Files to process : ' % len(files))
        for file in files:
            print("  - %s" % file)
        contents = ""
        files = sorted(files, key=lambda item: os.path.basename(item.lower().strip()))
        for file in files:
            with open(file) as f:
                contents += "\n\n---\n\n"
                contents += f.read()
        with Path.tempdir() as tmpdir:
            full_yaml_path = os.path.join(tmpdir, 'full_yaml.yml')
            with open(full_yaml_path, 'w+') as f:
                f.write(contents)
            context = {
                'self': self.env,
                'env': self.env,
                'user': self.env.user,
                '__global_context__': {},
            }
            index = 0
            for doc in yaml.load_all(open(full_yaml_path)):
                if doc:
                    index += 1
                    self._process_yaml_doc(index, doc, context, assets)
                    if auto_commit:
                        self.commit()
        if '__builtins__' in context: del context['__builtins__']
        return context

    def commit(self):
        self._require_env()
        self.env.cr.commit()

    def rollback(self):
        self._require_env()
        self.env.cr.rollback()

    def clear(self):
        self._require_env()
        if hasattr(self.env, 'invalidate_all'):
            self.env.invalidate_all()
        else:
            self.env.cache.invalidate()

    def dump_db(self, dest=False, zip=True):
        self._require_env()
        data_dir = os.path.join(self.odoo.tools.config["data_dir"], "backups", self.dbname)
        dest = dest or data_dir
        try:
            os.makedirs(dest)
        except:
            pass
        assert os.path.isdir(dest), "The directory [%s] should exists" % dest
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        ext = 'zip' if zip else 'dump'
        filename = "{}_{}.{}".format(self.dbname, now, ext)
        path = os.path.join(dest, filename)
        if self.list_db_disabled:
            self.list_db = True
        with open(path, 'wb+') as destination:
            kwargs = {}
            if not zip: kwargs['backup_format'] = 'custom'
            self.odoo.service.db.dump_db(self.dbname, destination, **kwargs)
        if self.list_db_disabled:
            self.list_db = False
        pprint('End: %s' % path)
        size = human_size(os.path.getsize(path))
        pprint('Size: %s' % size)
        return path

    def drop_db(self):
        try:
            self.odoo.service.db.exp_drop(self.dbname)
        except Exception as e:
            pass
        pprint('End: dbname=%s is dropped' % self.dbname)
        return self.dbname

    def restore_db(self, path, drop=False):
        assert os.path.isfile(path), 'The path [%s] sould be a file' % path
        if drop:
            self.drop_db()
        size = human_size(os.path.getsize(path))
        pprint('Size: %s' % size)
        self.odoo.service.db.restore_db(self.dbname, path)
        pprint('End: %s dbname=%s' % (path, self.dbname))
        return path


class Operator(object):
    @classmethod
    def flat(cls, *lists):
        result = []

        def put_in(item):
            if IF.is_iterable(item):
                for x in item:
                    put_in(x)
            else:
                result.append(item)

        for item in lists:
            put_in(item)
        return result

    @classmethod
    def unique(cls, sequence):
        result = []
        if IF.is_iterable(sequence):
            for item in sequence:
                found = False
                for res in result:
                    if res is item:
                        found = True
                        break
                if not found:
                    result.append(item)
        else:
            return sequence
        return result

    @classmethod
    def split_and_flat(cls, sep=',', *lists):
        result = cls.flat(lists)
        for i, item in enumerate(result):
            if IF.is_str(item):
                result[i] = item.split(sep)
        return cls.flat(result)

        def put_in(item):
            if IF.is_iterable(item):
                for x in item:
                    put_in(x)
            else:
                result.append(item)

        for item in lists:
            put_in(item)
        return result


class IF(object):
    @classmethod
    def is_xmlid(cls, text):
        if not cls.is_str(text) or cls.is_empty(text):
            return False
        else:
            text = text.strip()
            if re.match("^[a-z0-9_]+\.[a-z0-9_]+$", text):
                return True
            else:
                return False

    @classmethod
    def is_domain(cls, text):
        if not isinstance(text, list):
            return False
        ttuple, op = 0, 0
        for item in text:
            if isinstance(item, tuple):
                ttuple += 1
                if not (len(item) == 3 and isinstance(item[0], basestring) and isinstance(item[1], basestring)):
                    return False
            elif isinstance(item, basestring):
                op += 1
                if item not in ['&', '|', '!']:
                    return False
            else:
                return False
        if (op or ttuple) and op >= ttuple:
            return False
        return True

    @classmethod
    def is_str(cls, text):
        if isinstance(text, basestring):
            return True
        else:
            return False

    @classmethod
    def is_empty(cls, text):
        if cls.is_str(text):
            text = text.strip()
        if text:
            return False
        else:
            return True

    @classmethod
    def is_iterable(cls, text):
        if cls.is_str(text):
            return False
        if hasattr(text, '__iter__'):
            return True
        else:
            return False


class Eval(object):
    def __init__(self, data, context):
        self.data = data
        self.context = context or {}

    def eval(self, eval_result=True):
        def parse(value, ctx):
            if isinstance(value, list):
                return [parse(item, ctx) for item in value]
            elif isinstance(value, dict):
                _d = {}
                for _k, _v in value.items():
                    _d[_k] = parse(_v, ctx)
                return _d
            elif isinstance(value, basestring):
                origin = value
                res = value.format(**ctx)
                if origin != res and eval_result:
                    try:
                        res = eval(res, ctx)
                    except Exception as e:
                        pass
                return res
            else:
                return value

        return parse(self.data, self.context)


class SFTP(object):
    def __init__(self, sftp):
        self.sftp = sftp

    @contextmanager
    def chdir(self, path):
        try:
            origin = self.sftp.getcwd()
            self.sftp.chdir(path)
            yield
        except Exception as e:
            raise e
        finally:
            self.sftp.chdir(origin)


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
    @contextmanager
    def tempdir(cls):
        tmpdir = tempfile.mkdtemp()
        try:
            yield tmpdir
        finally:
            shutil.rmtree(tmpdir)

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
    def _clean_msg(self, msg):
        if not isinstance(msg, basestring):
            try:
                msg = unicode(msg)
            except:
                try:
                    msg = str(msg)
                except:
                    pass
        return msg

    def info(self, msg, exit=False):
        click.echo(self._clean_msg(msg))
        if exit:
            sys.exit(-1)

    def warn(self, msg, exit=False):
        click.secho(self._clean_msg(msg), fg='yellow')
        if exit:
            sys.exit(-1)

    def debug(self, msg, exit=False):
        click.secho(self._clean_msg(msg), fg='blue')
        if exit:
            sys.exit(-1)

    def success(self, msg, exit=False):
        click.secho(self._clean_msg(msg), fg='green')
        if exit:
            sys.exit(-1)

    def code(self, msg, exit=False):
        click.secho(self._clean_msg(msg), fg='cyan')
        if exit:
            sys.exit(-1)

    def error(self, msg, exit=True):
        click.secho(self._clean_msg(msg), fg='red')
        if exit:
            sys.exit(-1)

    def title(self, msg, exit=False):
        click.secho(self._clean_msg(msg), fg='white', bold=True)
        if exit:
            sys.exit(-1)


class File(object):
    @classmethod
    def get_size_str(cls, path, unit='mb'):
        size, u = cls._get_size(path, unit=unit)
        return "%s %s" % (size, u)

    @classmethod
    def get_size(cls, path, unit='mb'):
        size, u = cls._get_size(path, unit=unit)
        return size

    @classmethod
    def _get_size(cls, path, unit='mb'):
        size = os.path.getsize(path)
        if unit == 'mb':
            return round(size / (1024. * 1024.), 2), 'MB'
        else:
            return round(size, 2), 'B'
