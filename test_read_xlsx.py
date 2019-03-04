import os
from operator import itemgetter

import xlrd as xlrd
from past.types import basestring

from dyools import Date


y = Xlsx()
y.read(filename='gille tarifaire fournisseur.xls', sheets='TARIF')
tables = y.get_tables(['TARIF'])
table_3 = tables['TARIF'][2]

from pprint import pprint
#pprint(table_3)
#pprint(table_3.ncols)
#pprint(table_3.nrows)
#pprint(table_3.index_cols)
#pprint(table_3.index_rows)
#pprint(table_3.data)
table_3.set_col_idx([0, 1])
table_3.set_row_idx([1])
#pprint(table_3.index_cols)
#pprint(table_3.index_rows)
#pprint(table_3.get_value())
pprint(table_3.get_value_by_row_col(['40 - 50 kg'], ['10 - 20 mm', '21 - 22 µ']))
pprint(table_3.get_value_by_row_col(['71 - 80 kg'], ['21 - 30 mm', '23 - 24 µ']))
pprint(table_3[['71 - 80 kg']:['21 - 30 mm', '23 - 24 µ']])
pprint(table_3.get_value_by_idx(5,2))
pprint(table_3[5:2])

