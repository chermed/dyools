from __future__ import (absolute_import, division, print_function, unicode_literals)

import fnmatch
import os
import re
import shutil
import tempfile
from contextlib import contextmanager

from .klass_str import Str


class Print(object):

    def __init__(self, data):
        pass