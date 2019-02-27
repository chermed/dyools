from datetime import datetime

import xlsxwriter


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

    def _create_and_get_sheet(self, sheet_name=False):
        sheet_name = sheet_name or self.current_sheet or self.DEFAULT_SHEET_NAME
        for sheet_data in self.data:
            if sheet_data[self.SHEET_NAME] == sheet_name:
                return sheet_data
        sheet_data = {self.SHEET_NAME: sheet_name or self.DEFAULT_SHEET_NAME}
        self.data.append(sheet_data)
        sheet_data.setdefault('data', [])
        sheet_data.setdefault('header', [])
        sheet_data.setdefault('headers', [])
        sheet_data.setdefault('footer', {})
        sheet_data.setdefault('row', 0)
        sheet_data.setdefault('column', 0)
        sheet_data.setdefault('max_header', 0)
        sheet_data.setdefault('has_footer_name', False)
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
            return sum(data)/len(data)


    def set_offset(self, sheet_name=False):
        self._create_and_get_sheet(sheet_name)


    def set_sheet(self, row=0, col=0, sheet_name=False):
        sheet_data = self._create_and_get_sheet(sheet_name)
        sheet_data['row'] = row
        sheet_data['col'] = col


    def add_header(self, header, sheet_name=False):
        sheet_data = self._create_and_get_sheet(sheet_name)
        sheet_data['headers'].append(header)
        sheet_data['header'] = header
        sheet_data['max_header'] = len(header) if len(header) > sheet_data['max_header'] else sheet_data['max_header']


    def add_footer_name(self, name=False, sheet_name=False):
        sheet_data = self._create_and_get_sheet(sheet_name)
        sheet_data['footer_name'] = name or 'Total'
        sheet_data['has_footer_name'] = True

    def add_footer(self, column, operator, sheet_name=False):
        sheet_data = self._create_and_get_sheet(sheet_name)
        sheet_data['footer'].update({ column: operator})

    def add_line(self, line, sheet_name=False):
        assert isinstance(line, list), "The line should be a list"
        sheet_data = self._create_and_get_sheet(sheet_name)
        sheet_data['data'].append(line)


    def get(self):
        workbook = xlsxwriter.Workbook(self.filename)
        for sheet in self.data:
            sheet_name = sheet[self.SHEET_NAME]
            worksheet = workbook.add_worksheet(sheet_name)
            sheet_data = sheet['data']

            row = sheet['row']

            header_format = workbook.add_format()
            header_format.set_bold()
            header_format.set_text_wrap()
            header_format.set_border()
            header_format.set_bg_color('#CACFD2')
            infos = {}

            for header in sheet['headers']:
                col = sheet['column']
                if not header:
                    for i in range(sheet['max_header']):
                        worksheet.write(row, col, '', header_format)
                        col += 1
                else :
                    diff = sheet['max_header'] - len(header)
                    if diff:
                        worksheet.merge_range(row, col, row , col+ diff, header[0], header_format)
                        header = header[1:]
                        col += diff + 1
                    for i, cell_value in enumerate(header):
                        worksheet.write(row, col, cell_value, header_format)
                        infos[cell_value] = (i, col)
                        col += 1
                row += 1

            data_format = workbook.add_format()
            data_format.set_border()

            for line in sheet_data:
                col = sheet['column']
                for cell_value in line:
                    worksheet.write(row, col, cell_value, data_format)
                    col += 1
                row += 1

            footer_format = workbook.add_format()
            footer_format.set_bold()
            footer_format.set_border()
            footer_format.set_bg_color('yellow')
            col = sheet['column']
            for i in range(sheet['max_header']):
                worksheet.write(row, col, '', footer_format)
                col += 1
            for column, operator in sheet['footer'].items():
                idx, col = infos[column]
                cell_value = self._apply_op(idx, operator, sheet_name)
                worksheet.write(row, col, cell_value, footer_format)
            col = sheet['column']
            if sheet_data['has_footer_name'] :
                worksheet.write(row, col, sheet_data['has_footer_name'], footer_format)
            row += 1

        workbook.close()

    def save(self, path):
        pass


x = Xlsx()
x.add_header(['A', 'Z', 'H'])
x.add_header([])
x.add_header(['B1', 'B2', 'B3', 'B4', 'B5'])
x.add_header([])
x.add_header([])
x.add_line([10, 40, 10, 40, 10])
x.add_line([12, 32, 12, 32,12])
x.add_line([20, 30, 20, 30,20])
x.add_footer('B1', Xlsx.AVG)
x.add_footer('B2', x.SUM)
x.set_sheet('F1')
x.add_header(['B1', 'B2', 'B3', 'B4', 'B5'])
x.add_line([10, 40, 10, 40, 10])
x.add_line([12, 32, 12, 32,12])
x.add_footer('B4', Xlsx.AVG)
x.add_footer('B5', x.SUM)
from pprint import pprint
pprint(x.data)
x.get()
