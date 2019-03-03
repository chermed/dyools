import xlsxwriter

try:
    basestring
except NameError:
    basestring = str


class DF(object):
    def __init__(self, arg={}):
        assert isinstance(arg, list), "The argument should be a list"
        self.data = arg

    def add(self, name, data):
        self.data[name] = Serie(data)

    def remove(self, name):
        if name in self.data:
            del self.data[name]

    def __getitem__(self, item):
        return self.data[item]


class Serie(object):

    def __init__(self, arg):
        assert isinstance(arg, (list, Serie)), "The argument should be a list"
        if isinstance(arg, Serie):
            self.data = arg.data
        else:
            self.data = arg

    def __getitem__(self, item):
        assert isinstance(item, int), "the index should be an integer"
        return self.data[item]

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Serie([x + other for x in self.data])
        elif isinstance(other, Serie):
            return Serie([k + v for k, v in zip(self.data, other.data)])
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Serie([x - other for x in self.data])
        elif isinstance(other, Serie):
            return Serie([k - v for k, v in zip(self.data, other.data)])
        return self

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return Serie([other - x for x in self.data])
        elif isinstance(other, Serie):
            return Serie([v - k for k, v in zip(self.data, other.data)])
        return self

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Serie([x * other for x in self.data])
        elif isinstance(other, Serie):
            return Serie([k * v for k, v in zip(self.data, other.data)])
        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __floordiv__(self, other):
        if isinstance(other, (int, float)):
            return Serie([x / other for x in self.data])
        elif isinstance(other, Serie):
            return Serie([k / v for k, v in zip(self.data, other.data)])
        return self

    def __rfloordiv__(self, other):
        if isinstance(other, (int, float)):
            return Serie([other / x for x in self.data])
        elif isinstance(other, Serie):
            return Serie([v / k for k, v in zip(self.data, other.data)])
        return self

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Serie([x / other for x in self.data])
        elif isinstance(other, Serie):
            return Serie([k / v for k, v in zip(self.data, other.data)])
        return self

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return Serie([other / x for x in self.data])
        elif isinstance(other, Serie):
            return Serie([v / k for k, v in zip(self.data, other.data)])
        return self

    def __div__(self, other):
        if isinstance(other, (int, float)):
            return Serie([x / other for x in self.data])
        elif isinstance(other, Serie):
            return Serie([k / v for k, v in zip(self.data, other.data)])
        return self

    def __rdiv__(self, other):
        if isinstance(other, (int, float)):
            return Serie([other / x for x in self.data])
        elif isinstance(other, Serie):
            return Serie([v / k for k, v in zip(self.data, other.data)])
        return self

    def __pow__(self, power, modulo=None):
        return Serie([pow(x, power) for x in self.data])

    def __str__(self):
        return "<Serie %s>" % self.data

    def __repr__(self):
        return "<Serie %s>" % self.data


class Xlsx(object):
    AVG = 'avg'
    SUM = 'sum'
    MIN = 'min'
    MAX = 'max'
    DEFAULT_SHEET_NAME = 'Feuil1'
    SHEET_NAME = 'sheet_name'

    def __init__(self):
        self.data = []
        self.filename = "File_TODO.xlsx"
        self.current_sheet = False
        self.num_format = '#,##0.00'
        self.format_header = {'bold': True, 'bg_color': '#D9D9D9',  'border': True}
        self.format_footer= {'bold': True, 'bg_color': 'yellow',  'border': True}
        self.format_int = { 'border': True}
        self.format_str = { 'border': True}
        self.format_float = {'num_format' : '#,##0.00' ,'border': True}
        self.column_str_width = 30
        self.column_nonstr_width = 16

    def _create_and_get_sheet(self, sheet_name=False):
        sheet_name = sheet_name or self.current_sheet or self.DEFAULT_SHEET_NAME
        for sheet_data in self.data:
            if sheet_data[self.SHEET_NAME] == sheet_name:
                self.current_sheet = sheet_data[self.SHEET_NAME]
                return sheet_data
        sheet_data = {self.SHEET_NAME: sheet_name or self.DEFAULT_SHEET_NAME}
        self.data.append(sheet_data)
        sheet_data.setdefault('data', [])
        sheet_data.setdefault('header', [])
        sheet_data.setdefault('headers', [])
        sheet_data.setdefault('main_header', [])
        sheet_data.setdefault('types', {-1: 'str'})
        sheet_data.setdefault('footer', {})
        sheet_data.setdefault('row', 0)
        sheet_data.setdefault('column', 0)
        sheet_data.setdefault('max_header', 0)
        sheet_data.setdefault('has_footer_name', False)
        sheet_data.setdefault('has_totals', False)
        self.current_sheet = sheet_data[self.SHEET_NAME]
        return sheet_data

    def _apply_op(self, idx, op, sheet_name=False):
        sheet_data = self._create_and_get_sheet(sheet_name)
        data = [x[idx] for x in sheet_data['data']]
        if not data:
            return False
        elif op == self.MIN:
            return min(data)
        elif op == self.MAX:
            return max(data)
        elif op == self.SUM:
            return sum(data)
        elif op == self.AVG:
            return sum(data) / len(data)

    def _get_column_idx(self, column, sheet_name=False):
        if isinstance(column, int):
            return column
        sheet_data = self._create_and_get_sheet(sheet_name)
        for header_tab in sheet_data['headers']:
            for header in header_tab:
                if column in header:
                    return header.index(column)
        return -1

    def set_offset(self, row=0, col=0, sheet_name=False):
        sheet_data = self._create_and_get_sheet(sheet_name)
        sheet_data['row'] = row
        sheet_data['column'] = col

    def set_sheet(self, sheet_name=False):
        self._create_and_get_sheet(sheet_name)

    def add_sheet(self, sheet_name=False):
        self._create_and_get_sheet(sheet_name)
        self.set_sheet(sheet_name)

    def add_header(self, header, sheet_name=False):
        sheet_data = self._create_and_get_sheet(sheet_name)
        sheet_data['headers'].append(header)
        sheet_data['header'] = header
        max_header = sheet_data['max_header']
        max_header = len(header) if len(header) > max_header else max_header
        sheet_data['max_header'] = max_header
        sheet_data['main_header'] = header if len(header) == max_header else sheet_data.get('main_header', [])

    def add_footer_name(self, name=False, sheet_name=False):
        sheet_data = self._create_and_get_sheet(sheet_name)
        sheet_data['footer_name'] = name or 'Total'
        sheet_data['has_footer_name'] = True

    def add_footer(self, column, operator, sheet_name=False):
        sheet_data = self._create_and_get_sheet(sheet_name)
        if isinstance(column, basestring):
            column = self._get_column_idx(column, sheet_name)
        sheet_data['footer'].update({column: operator})

    def add_totals(self, sheet_name=False):
        sheet_data = self._create_and_get_sheet(sheet_name)
        sheet_data['has_totals'] = True

    def add_column(self, col_name, col_data, sheet_name=False):
        assert isinstance(col_name, basestring), "The column name should be a string"
        assert isinstance(col_data, (list, Serie)), "The column data should be a list or a serie"
        sheet_data = self._create_and_get_sheet(sheet_name)
        sheet_data['main_header'].append(col_name)
        sheet_data['max_header'] += 1
        sheet_data['types'].setdefault(len(sheet_data['main_header']) - 1, 'str')
        for i, line in enumerate(sheet_data['data']):
            line.append(col_data[i])

    def add_line(self, line, sheet_name=False):
        assert isinstance(line, list), "The line should be a list"
        sheet_data = self._create_and_get_sheet(sheet_name)
        sheet_data['data'].append(line)
        max_header = sheet_data['max_header']
        max_header = len(line) if len(line) > max_header else max_header
        sheet_data['max_header'] = max_header

    def _reset_types(self, sheet_name=False):
        sheet_data = self._create_and_get_sheet(sheet_name)
        data = sheet_data['data']
        for i in range(sheet_data['max_header']):
            sheet_data['types'].setdefault(i, 'str')
        for line in data:
            for i, cell in enumerate(line):
                sheet_data['types'].setdefault(i, 'str')
                if sheet_data['types'][i] == 'str':
                    if isinstance(cell, int):
                        sheet_data['types'][i] = 'int'
                    elif isinstance(cell, float):
                        sheet_data['types'][i] = 'float'
        return sheet_data['types']

    def get(self):
        def write_value(row, col, cell_value, place='data', ttype='str', merge=False):
            if place == 'header':
                fmt = workbook.add_format(self.format_header)
            elif place == 'footer':
                fmt = workbook.add_format(self.format_footer)
            elif ttype == 'int':
                fmt = workbook.add_format(self.format_int)
            elif ttype == 'float':
                fmt = workbook.add_format(self.format_float)
            else:
                fmt = workbook.add_format(self.format_str)
            if isinstance(merge, tuple) and len(merge) == 2:
                worksheet.merge_range(row, col, merge[0], merge[1], cell_value, fmt)
            else:
                worksheet.write(row, col, cell_value, fmt)

        def get_type(sheet, column, default='str'):
            if isinstance(column, basestring):
                column = sheet['main_header'].index(column) if column in sheet['main_header'] else -1
            return sheet['types'].get(column, default)

        workbook = xlsxwriter.Workbook(self.filename)
        for sheet in self.data:
            col = sheet['column']
            row = sheet['row']
            sheet_name = sheet[self.SHEET_NAME]
            ttypes = self._reset_types(sheet_name)
            worksheet = workbook.add_worksheet(sheet_name)
            for i in range(sheet['max_header']):
                if ttypes[i] == 'str':
                    worksheet.set_column(i+col, i+col, self.column_str_width)
                else:
                    worksheet.set_column(i+col, i+col, self.column_nonstr_width)
            sheet_data = sheet['data']
            infos = {}
            for header in sheet['headers']:
                col = sheet['column']
                if not header:
                    for i in range(sheet['max_header']):
                        write_value(row, col, ' ', 'header', 'str')
                        col += 1
                else:
                    diff = sheet['max_header'] - len(header)
                    if diff:
                        write_value(row, col, header[0], 'header', 'str', merge=(row, col + diff))
                        header = header[1:]
                        infos[header[0]] = (col, col)
                        col += diff + 1
                    for i, cell_value in enumerate(header):
                        write_value(row, col, cell_value, 'header', 'str')
                        col += 1
                row += 1
            for i in range(sheet['max_header']):
                infos[i] = (i, i+sheet['column'])
            for line in sheet_data:
                col = sheet['column']
                for i, cell_value in enumerate(line):
                    write_value(row, col, cell_value, 'data', ttypes[i])
                    col += 1
                row += 1
            col = sheet['column']
            if sheet['has_totals']:
                for i in range(sheet['max_header']):
                    sheet['footer'][i] = self.SUM
            if sheet['footer'] or sheet['has_totals']:
                for i in range(sheet['max_header']):
                    write_value(row, col, ' ', 'footer', 'str')
                    col += 1
                for column, operator in sheet['footer'].items():
                    ttype = get_type(sheet, column, 'str')
                    if ttype != 'str':
                        idx, col = infos[column]
                        cell_value = self._apply_op(idx, operator, sheet_name)
                        write_value(row, col, cell_value, 'footer', get_type(sheet, column))
            col = sheet['column']
            if sheet['has_footer_name']:
                write_value(row, col, sheet['footer_name'], 'footer')
            row += 1
        workbook.close()

    def __getitem__(self, item):
        sheet_data = self._create_and_get_sheet()
        idx = item if isinstance(item, int) else None
        if idx is None:
            for i, header in enumerate(sheet_data['main_header']):
                if header == item:
                    idx = i
                    break
        assert isinstance(idx, int), "The index [%s] should be integer" % idx
        return Serie([x[idx] for x in sheet_data['data']])


x = Xlsx()
x.add_header(['DEVIS', 'S0777'])

x.add_header(['Article', 'Quantité', 'Prix unitaire'])
x.add_header([])
x.add_line(["Iphone", 3, 900.01])
x.add_line(["Ipad", 3, 200])
x.add_line(["Imac", 1, 2000])
x.add_totals()
x.add_column('Prix HT', x['Quantité'] * x['Prix unitaire'])
x.add_footer_name('XXX TOTAL XXX')
x.set_sheet('Test 6-8')
x.set_offset(6, 8)
x.add_header(['DEVIS', 'S0777'])

x.add_header(['Article', 'Quantité', 'Prix unitaire'])
x.add_header([])
x.add_line(["Iphone", 3, 900.01])
x.add_line(["Ipad", 3, 200])
x.add_line(["Imac", 1, 2000])
x.add_totals()
x.add_column('Prix HT', x['Quantité'] * x['Prix unitaire'])
x.add_footer_name('XXX TOTAL XXX')
from pprint import pprint
x.add_sheet('SANS Header')
x.add_line(["Iphone", 3, 900.01])
x.add_line(["Ipad", 3, 200])
x.add_line(["Imac", 1, 2])
x.add_totals()
x.add_sheet('SANS footer')
x.add_header(['Article', 'Quantité', 'Prix unitaire'])
x.add_line(["Iphone", 3, 900.01])
x.add_line(["Ipad", 3, 200])
x.add_line(["Imac", 1, 2])
x.add_sheet('Jsut Data')
x.add_line(["Iphone", 3, 900.01])
x.add_line(["Ipad", 3, 200])
x.add_line(["Imac", 1, 2])

x.add_sheet('Just headers')
x.add_header(['DEVIS', 'S0777'])

x.add_header(['Article', 'Quantité', 'Prix unitaire'])
x.add_header([])
x.add_sheet('Just footer')
x.add_totals()

x.add_sheet('Header + footer ')
x.add_header(['DEVIS', 'S0777'])

x.add_header(['Article', 'Quantité', 'Prix unitaire'])
x.add_header([])
x.add_totals()
x.add_footer('Article', x.SUM)

pprint(x.data)
pprint(x.data)
x.get()
