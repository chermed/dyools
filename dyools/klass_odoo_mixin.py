from __future__ import (absolute_import, division, print_function, unicode_literals)

import importlib
import logging
import os
from functools import partial

import odoorpc
from past.builtins import basestring
from prettytable import PrettyTable

from .klass_path import Path
from .klass_tool import Tool

logger = logging.getLogger(__name__)


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

    def vlist(self, records, fields=[], types=[], title=False):
        return self.show(records, fields, types, title, vlist=True)

    def hlist(self, records, fields=[], types=[], title=False):
        return self.show(records, fields, types, title, vlist=False)

    def data(self, records, fields=[], types=[], title=False, vlist=True):
        return self._show_data(records, fields, types, title, vlist, _show_data=False)

    def show(self, records, fields=[], types=[], title=False, vlist=True):
        return self._show_data(records, fields, types, title, vlist, _show_data=True)

    def _show_data(self, records, fields=[], types=[], title=False, vlist=True, _show_data=True):
        self._require_env()
        if isinstance(types, basestring):
            types = types.split()
        if isinstance(fields, basestring):
            fields = fields.split()
        assert isinstance(fields, list), 'fields should be a list'
        if title:
            print('@@@@ %s @@@@' % title)
        print('Show %s record(s)' % len(records))
        if isinstance(records, dict):
            new_records = []
            for rk, rv in records.items():
                rv.update(dict(name=rk))
                new_records.append(rv)
            records = new_records
        if not fields:
            if isinstance(records, odoorpc.models.Model):
                fields = list(self.env[records._name].fields_get().keys())
            elif isinstance(records, list):
                fields = records[0].keys() if records else ['name']
            else:
                fields = list(records.fields_get().keys())
        if types and not isinstance(records, list):
            if isinstance(records, odoorpc.models.Model):
                fields_get = self.env[records._name].fields_get()
            else:
                fields_get = records.fields_get()
            fields = filter(lambda f: '.' not in f and fields_get[f]['type'] in types, fields)
        fields = list(fields)
        if fields:
            if 'id' not in fields:
                fields = ['id'] + fields
            if not isinstance(records, list):
                records = records.read(fields)
            if vlist:
                tbl_data = [fields]
                for record in records:
                    tbl_data.append([record.get(f, '') for f in fields])
            else:
                tbl_data = [['field', 'value']]
                for record in records:
                    tbl_data.append(['---', '---'])
                    for f in fields:
                        tbl_data.append([f, record.get(f, '')])
        if _show_data:
            if not fields:
                print('No field found')
            else:
                if tbl_data:
                    x = PrettyTable()
                    x.field_names = tbl_data[0]
                    for item in tbl_data[1:]:
                        x.add_row(item)
                    print(x)
                print('Total: %s' % (len(tbl_data) - 1))
        else:
            return tbl_data

    def path(self, module):
        if isinstance(module, basestring):
            module = importlib.import_module(module)
        return os.path.dirname(module.__file__)

    def get(self, model, domain=[], limit=False, order=False, **kwargs):
        self._require_env()
        records = model
        if isinstance(domain, int):
            domain = [('id', '=', domain)]
        elif isinstance(domain, tuple):
            domain = [domain]
        if isinstance(domain, basestring) and len(domain.split()) < 3:
            domain = [('name', '=', domain)]
        elif isinstance(domain, basestring):
            domain = Tool.contruct_domain_from_str(domain)
        for d_key, d_value in kwargs.items():
            domain.append((d_key, '=', d_value))
        if hasattr(self.odoo, 'models') and isinstance(records, self.odoo.models.Model):
            domain = ['&', ('id', 'in', records.ids)] + domain
            model = records._name
        if isinstance(records, odoorpc.models.Model):
            domain = ['&', ('id', 'in', records.ids)] + domain
            model = records._name
        search_kwargs = {}
        if limit: search_kwargs['limit'] = limit
        if order: search_kwargs['order'] = order
        res = self.env[model].search(domain, **search_kwargs)
        res = self.obj(model, res)
        return res

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

    def config(self, **kwargs):
        model = 'res.config.settings'
        res = self.env[model].create(kwargs)
        res = self.obj(model, res)
        res.execute()

    def obj(self, model, res):
        if isinstance(res, (int, list)):
            return self.env[model].browse(res)
        return res

    def ref(self, xmlid, raise_if_not_found=True):
        self._require_env()
        return self.env.ref(xmlid)

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

    def fields(self, model, fields=[]):
        self._require_env()
        if fields and isinstance(fields, basestring):
            fields = fields.split()
        if not isinstance(model, basestring):
            model = model._name
        if fields:
            columns = fields
            ffields = self.env[model].fields_get()
        else:
            columns = ['name', 'ttype', 'relation', 'modules']
            ffields = self.get('ir.model.fields', [('model_id.model', '=', model)])
        self.show(ffields, columns)

    def menus(self, debug=False, xmlid=False, action=False, user=False):
        self._require_env()
        lines = []

        def menu_show(menu, level):
            space = (' ' * 4 * (level - 1)) if level > 1 else ''
            if space:
                space = '|' + space[1:]
            bar = ('|' + '-' * 3) if level > 0 else ''
            fmt = "{space}{bar} {name}"
            action_model = action_domain = action_context = False
            if xmlid:
                fmt += '  XMLID={xmlid}'
            if action:
                if menu.get('action'):
                    action_env, action_id = menu.get('action').split(',')
                    [action_dict] = self.env[action_env].browse(int(action_id)).read(['res_model', 'domain', 'context'])
                    if action_dict:
                        action_model = action_dict.get('res_model') or ''
                        if action_model:
                            fmt += '  Model={action_model}'
                        action_domain = action_dict.get('domain') or []
                        if action_domain:
                            fmt += '  Domain={action_domain}'
                        action_context = action_dict.get('context') or {}
                        if action_context:
                            fmt += '  Context={action_context}'
            line = fmt.format(
                space=space,
                bar=bar,
                menu=menu,
                name=menu['name'],
                xmlid=menu.get('xmlid') or '',
                action_model=action_model,
                action_domain=action_domain,
                action_context=action_context,
            )
            lines.append(line)
            for m in menu.get('children', []):
                menu_show(m, level=level + 1)

        if user:
            user = self.get_users(user)
            menus = self.env['ir.ui.menu'].sudo(user.id).load_menus(debug=debug)
        else:
            menus = self.env['ir.ui.menu'].load_menus(debug=debug)
        for menu in menus.get('children', []):
            menu_show(menu, level=0)
        for line in lines:
            print(line)

    def __getitem__(self, item):
        self._require_env()
        return self.env[item]

    def __getattr__(self, item):
        mapping = {
            'warhouses': 'stock.warehouse',
            'companies': 'res.company',
            'users': 'res.users',
            'partners': 'res.partner',
            'products': 'product.product',
            'templates': 'product.template',
            'sales': 'sale.order',
            'invoices': 'account.invoice',
            'purchases': 'purchase.order',
            'quants': 'stock.quant',
            'pickings': 'stock.picking',
            'operations': 'stock.picking.type',
            'locations': 'stock.location',
            'amls': 'account.move.line',
        }
        if item.startswith('get_'):
            self._require_env()
            _item = item[4:]
            model = False
            if _item in mapping.keys():
                model = mapping[_item]
            elif _item.endswith('ies'):
                _item = _item[:-3] + 'y'
            elif _item.endswith('s'):
                _item = _item[:-1]
            if _item in mapping.keys():
                model = mapping[_item]
            model = model or _item.replace('_', '.')
            if model:
                return partial(self.get, model)
        return super(Mixin, self).__getattr__(item)

    def __lshift__(self, other):
        assert isinstance(other, Mixin), "Backup and restore work for environnements"
        with Path.tempdir() as tmp:
            path = other.dump_db(dest=tmp)
            self.restore_db(path, drop=True)

    def __rshift__(self, other):
        assert isinstance(other, Mixin), "Backup and restore work for environnements"
        with Path.tempdir() as tmp:
            path = self.dump_db(dest=tmp)
            other.restore_db(path, drop=True)
