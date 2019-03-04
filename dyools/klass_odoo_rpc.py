from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
from datetime import datetime
from urllib import parse
from urllib.parse import urlparse

import odoorpc

from .klass_file import File
from .klass_odoo_mixin import Mixin


class RPC(Mixin):
    def __init__(self, *args, **kwargs):
        items = ['host', 'port', 'dbname', 'user', 'password', 'superadminpassword', 'protocol', 'ssl']
        for i, arg in enumerate(args):
            kwargs[items[i]] = arg
        server = kwargs.get('server') or (args and args[0]) or False
        server = os.environ.get(kwargs['from_env']) if kwargs.get('from_env') else server
        if server:
            url = urlparse(server)
            if url.scheme and url.netloc and url.query:
                kwargs.update(dict(parse.parse_qsl(url.query)))
                url_ssl = False
                if url.scheme.endswith('s'):
                    kwargs['ssl'] = True
                    url_ssl = True
                url_loc = url.netloc.split(':')
                kwargs['host'] = url_loc[0]
                kwargs['port'] = int(url_loc[1]) if len(url_loc) == 2 else (443 if url_ssl else 80)
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
        kwargs.update(dict(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            superadminpassword=superadminpassword,
            protocol=protocol,
            timeout=timeout,
        ))
        self.kwargs = kwargs

    def login(self, user=False, password=False, dbname=False):
        if user:
            self.user = user
        if password:
            self.password = password
        if dbname:
            self.dbname = dbname
        self.kwargs.update({
            'dbname': self.dbname,
            'user': self.user,
            'password': self.password,
        })
        assert self.user and self.password, "please provide the user and the password"
        self.odoo.login(self.dbname, self.user, self.password)
        self.env = self.odoo.env
        return self.env

    def infos(self):
        print(
            "Host: {host}\nPort: {port}\nDatabase: {dbname}\nUser: {user}\nPassword: {password}\nSuperAdminPassword: {superadminpassword}\nProtocol: {protocol}\nTimeout: {timeout}".format(
                **self.kwargs))

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
        print('End: %s' % path)
        size = File.get_size_str(path)
        print('Backup Size: %s' % size)
        return path

    def drop_db(self):
        if self.dbname in self.list_db():
            self.odoo.db.drop(self.superadminpassword, self.dbname)
            print('End: dbname=%s is dropped' % self.dbname)
        else:
            print('The database [%s] is not found' % self.dbname)
        return self.dbname

    def restore_db(self, path, drop=False):
        assert os.path.isfile(path), 'The path [%s] sould be a file' % path
        if drop:
            self.drop_db()
        size = File.get_size_str(path)
        print('Restore Size: %s' % size)
        with open(path, 'rb') as dump_zip:
            self.odoo.db.restore(self.superadminpassword, self.dbname, dump_zip)
        print('End: %s dbname=%s' % (path, self.dbname))
        return path

    def list_db(self):
        res = self.odoo.db.list()
        print(res)
        return res