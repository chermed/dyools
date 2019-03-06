from __future__ import (absolute_import, division, print_function, unicode_literals)

import itertools
from operator import itemgetter

from past.builtins import basestring


class Table(object):
    def __init__(self, data):
        self.data = data
        self.col_idx = []
        self.row_idx = []
        self.nrows = len(data)
        self.ncols = len(data[0]) if data else 0
        self.index_rows = [[x for x in range(self.nrows)]]
        self.index_cols = [[x for x in range(self.ncols)]]

    def set_col_idx(self, idx):
        assert idx and isinstance(idx, list), "The indexes should be a non empty list"
        self.col_idx = idx
        self._reindex()

    def set_row_idx(self, idx):
        assert idx and isinstance(idx, list), "The indexes should be a non empty list"
        self.row_idx = idx
        self._reindex()

    def get_row_by_idx(self, idx):
        assert isinstance(idx, int), 'The index [%s] should be an integer' % idx
        return self.data[idx]

    def get_col_by_idx(self, idx):
        assert isinstance(idx, int), 'The index [%s] should be an integer' % idx
        return list(map(itemgetter(idx), self.data))

    def _reindex(self):
        rows = []
        cols = []
        for row_idx in self.row_idx:
            rows.append(self.get_row_by_idx(row_idx))
        if not rows:
            rows.append([x for x in range(self.nrows)])
        for col_idx in self.col_idx:
            cols.append(self.get_col_by_idx(col_idx))
        if not cols:
            cols.append([x for x in range(self.ncols)])
        self.index_rows = rows
        self.index_cols = cols

    def get_value_by_idx(self, row_idx, col_idx):
        assert isinstance(row_idx, int) and isinstance(col_idx, int), "the index should be an integer"
        assert row_idx < self.nrows, "the index is out of range"
        assert col_idx < self.ncols, "the index is out of range"
        return self.data[row_idx][col_idx]

    def get_value_by_row_col(self, row_idx=[], col_idx=[]):
        if isinstance(row_idx, basestring):
            row_idx = row_idx.split(';')
        if isinstance(col_idx, basestring):
            col_idx = col_idx.split(';')
        assert len(row_idx) == len(self.index_rows), "please provide the same number of rows indexes"
        assert len(col_idx) == len(self.index_cols), "please provide the same number of columns indexes"
        row_tuples = list(zip(row_idx, self.index_rows))
        col_tuples = list(zip(col_idx, self.index_cols))
        row_indices = []
        for i, line in row_tuples:
            _row_indices = [x for x, y in enumerate(line) if y == i]
            if row_indices:
                row_indices = list(set(row_indices) & set(_row_indices))
            else:
                row_indices = _row_indices
        col_indices = []
        for i, line in col_tuples:
            _col_indices = [x for x, y in enumerate(line) if y == i]
            if col_indices:
                col_indices = list(set(col_indices) & set(_col_indices))
            else:
                col_indices = _col_indices
        assert col_indices and row_indices, "can not found the indexes for col=%s and row=%s" % (col_idx, row_idx)
        row_indices, col_indices = row_indices[0], col_indices[0]
        for i, row in enumerate(self.data):
            for j, col in enumerate(self.data[i]):
                if i == col_indices and j == row_indices:
                    return self.data[i][j]
        return None

    def get_flat(self, empty=True):
        tables = []
        for row_tuple in itertools.product(*self.index_rows):
            for col_tuple in itertools.product(*self.index_cols):
                value = self[row_tuple:col_tuple]
                if not empty:
                    if isinstance(value, basestring):
                        if not value.strip():
                            continue
                    if not value:
                        continue
                line = list(row_tuple) + list(col_tuple) + [value]
                tables.append(line)
        return tables

    def __getitem__(self, item):
        if isinstance(item, slice):
            if isinstance(item.start, int) and isinstance(item.stop, int):
                return self.get_value_by_idx(item.start, item.stop)
            else:
                return self.get_value_by_row_col(item.start, item.stop)
        elif isinstance(item, int):
            return self.get_col_by_idx(item)
        raise IndexError()
