from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
import shutil
import tempfile
from contextlib import contextmanager


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

    @classmethod
    def create_file(cls, path, content):
        def _erase_data(_path, _content):
            with open(_path, 'w+') as f:
                f.write(_content)

        if not os.path.isfile(path):
            ddir = os.path.dirname(path)
            Path.create_dir(ddir)
            _erase_data(path, content)
        else:
            with open(path, 'r') as f:
                c = f.read()
            if c != content:
                _erase_data(path, content)

    @classmethod
    def create_dir(cls, path):
        if not os.path.isdir(path):
            os.makedirs(path)

    @classmethod
    def clean_dir(cls, path):
        if os.path.exists(path):
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                elif os.path.isfile(full_path):
                    os.remove(full_path)

    @classmethod
    def delete_path(cls, path):
        if os.path.exists(path):
            shutil.rmtree(path)
