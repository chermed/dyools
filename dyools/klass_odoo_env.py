from __future__ import (absolute_import, division, print_function, unicode_literals)

import base64
import os
import sys
from datetime import datetime, date

import yaml
from dateutil.parser import parse as dtparse
from past.builtins import basestring

from .klass_eval import Eval
from .klass_is import IS
from .klass_odoo_mixin import Mixin
from .klass_path import Path

DATE_FORMAT, DATETIME_FORMAT = "%Y-%m-%d", "%Y-%m-%d %H:%M:%S"


class Env(Mixin):
    def __init__(self, env=False, odoo=False, dbname=False, verbose=True):
        if isinstance(env, basestring):
            dbname = env
            env = False
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
        if not addons_path:
            addons_path = []
        elif isinstance(addons_path, basestring):
            addons_path = addons_path.split(',')
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
        print('Installed modules   : %s' % installed)
        print('Uninstalled modules : %s' % uninstalled)
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
            elif isinstance(value, list) and IS.domain(value):
                ids = self.env[relation].search(value).ids
            elif isinstance(value, int):
                ids = [value]
            elif isinstance(value, basestring):
                if IS.xmlid(value):
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

    def _process_config(self, value):
        return self.env['res.config.settings'].create(value).execute()

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
            elif IS.xmlid(refs):
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
                if isinstance(refs, basestring) and IS.xmlid(refs):
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
            elif key == 'config':
                print("[%s] ***** Configuration *****" % index)
                self._process_config(value)

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
                assert os.path.exists(path), "The path [%s] should exists" % path
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
        print('End: %s' % path)
        size = Path.get_size_str(path)
        print('Backup Size: %s' % size)
        return path

    def drop_db(self):
        if self.dbname in self.list_db():
            self.odoo.service.db.exp_drop(self.dbname)
            print('End: dbname=%s is dropped' % self.dbname)
        else:
            print('The database [%s] is not found' % self.dbname)
        return self.dbname

    def restore_db(self, path, drop=False):
        assert os.path.isfile(path), 'The path [%s] should be a file' % path
        if drop:
            try:
                self.drop_db()
            except:
                print('can not drop the database')
        size = Path.get_size_str(path)
        print('Restore Size: %s' % size)
        self.odoo.service.db.restore_db(self.dbname, path)
        print('End: %s dbname=%s' % (path, self.dbname))
        return path

    def list_db(self):
        res = self.odoo.service.db.list_dbs()
        print(res)
        return res
