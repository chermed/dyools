from __future__ import (absolute_import, division, print_function, unicode_literals)

from pprint import pprint

import requests
from past.builtins import basestring
from prettytable import PrettyTable

CONSOLE, CMDLINE = 'console', 'cmdline'


class Consumer(object):
    def __init__(self, host='127.0.0.1', port=5000, token=None):
        self.host = host
        self.port = port
        self.token = token
        self.data = []

    def _send(self, mode):
        assert mode in ['console', 'cmdline'], 'The mode [%s] is not implemented' % mode
        headers = {'WS_TOKEN': self.token}
        res = requests.post('http://%s:%s' % (self.host, self.port), json={mode: self.data}, headers=headers)
        self.result = res.json()
        return self.result

    def stop(self):
        headers = {'WS_TOKEN': self.token}
        res = requests.post('http://%s:%s/shutdown' % (self.host, self.port), json={}, headers=headers)
        self.result = res.json()
        return self.result

    def ping(self):
        headers = {'WS_TOKEN': self.token}
        res = requests.post('http://%s:%s/ping' % (self.host, self.port), json={}, headers=headers)
        self.result = res.json()
        return self.result

    def info(self):
        headers = {'WS_TOKEN': self.token}
        res = requests.post('http://%s:%s/info' % (self.host, self.port), json={}, headers=headers)
        self.result = res.json()
        return self.result

    def cmdline(self):
        return self._send(CMDLINE)

    def console(self):
        return self._send(CONSOLE)

    def print(self):
        data = self.result['data']
        if isinstance(data, basestring):
            for line in data.replace('\\n', '\n').split('\n'):
                print(line)
        else:
            pprint(data)

    def add(self, *args):
        self.data.extend(args)

    def flush(self):
        self.data = []
        self.result = ""

    def __getattr__(self, item):
        if item.startswith('table_'):
            item = item[6:]
            tbl_data = self.result[item]
            x = PrettyTable()
            x.field_names = tbl_data[0]
            for item in tbl_data[1:]:
                x.add_row(item)
            print(x)
            print('Total: %s' % (len(tbl_data) - 1))
            return lambda: 'End'
        elif item.startswith('print_'):
            item = item[6:]
            tbl_data = self.result[item]
            pprint(tbl_data)
            print('Total: %s' % len(tbl_data))
            return lambda: 'End'
        elif item.startswith('data_'):
            item = item[6:]
            tbl_data = self.result[item]
            return lambda: tbl_data
        else:
            return super(Consumer, self).__getattr__(item)
