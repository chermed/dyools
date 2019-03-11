from prettytable import PrettyTable

from .klass_is import IS


class Data(object):

    def __init__(self, data, has_header=True, header=[]):
        header, lines = self._normalize_origin(data, has_header, header)
        self.lines = lines[::]
        self.header = header[::]

    def _normalize_origin(self, data, has_header, header):
        if not data:
            data = []
        lines = []
        if IS.dict_of_dict(data):
            origin = data.copy()
            header = ['name']
            for key, values in origin.items():
                line = [key]
                for k in sorted(values.keys()):
                    line.append(values[k])
                    if k not in header:
                        header.append(k)
                lines.append(line)
        elif IS.dict_of_values(data):
            header = sorted(list(data.keys()))
            lines = [data[k] for k in header]
        elif IS.list_of_dict(data):
            origin = data[::]
            header = []
            lines = []
            for item in origin:
                line = []
                for key in sorted(item.keys()):
                    if key not in header:
                        header.append(key)
                    line.append(item[key])
                lines.append(line)
        elif IS.list_of_list(data):
            origin = data[::]
            if origin and has_header and not header:
                header = origin[0]
                lines = origin[1:]
            else:
                lines = origin
        elif IS.list_of_values(data):
            origin = data[::]
            if origin and has_header and not header:
                header = origin
                lines = []
            else:
                lines = [origin]
        return header, lines

    def get_lines(self):
        return self.lines

    def get_header(self):
        header = self.header
        if not header and self.lines:
            header = [x for x in range(len(self.lines[0]))]
        return header

    def get_pretty_table(self):
        tbl_data = self.to_list()
        x = PrettyTable()
        x.field_names = tbl_data[0]
        for item in self.get_lines():
            x.add_row(item)
        return x

    def to_list(self):
        res = []
        if self.header:
            res.append(self.header)
        if self.lines:
            res.append(self.lines)
        return res

    def to_dictlist(self):
        header = self.header
        res = []
        if not header and self.lines:
            header = [x for x in range(len(self.lines[0]))]
        for line in self.lines:
            if IS.list_of_list(line):
                for item in line:
                    res.append({k: v for k, v in zip(header, item)})
            else:
                res.append({k: v for k, v in zip(header, line)})
        return res
