from unittest import TestCase


class TestData(TestCase):
    def test_data_empty(self):
        from dyools import Data
        self.assertEqual(Data({}, has_header=False).to_list(), [])
        self.assertEqual(Data([], has_header=False).to_list(), [])
        self.assertEqual(Data({}, has_header=False).to_dictlist(), [])
        self.assertEqual(Data([], has_header=False).to_dictlist(), [])
        self.assertEqual(Data(False, has_header=False).to_list(), [])
        self.assertEqual(Data(None, has_header=False).to_list(), [])
        self.assertEqual(Data([[], []], has_header=False).to_list(), [[[], []]])
        self.assertEqual(Data([[], []], has_header=True).get_lines(), [[]])
        self.assertEqual(Data([[], []], has_header=True).get_header(), [])

    def test_data_dict_of_dict(self):
        out_header = ['name', 'arg1', 'arg2', 'arg3']
        out_lines = [
            ['key1', 'value1', 'value2', 'value3'],
            ['key2', 'value6', 'value5', 'value4'],
            ['key3', 'value7', 'value8', 'value9'],
        ]
        dict_of_dict = {
            'key1': {
                'arg1': 'value1',
                'arg3': 'value3',
                'arg2': 'value2',
            },
            'key2': {
                'arg1': 'value6',
                'arg2': 'value5',
                'arg3': 'value4',
            },
            'key3': {
                'arg1': 'value7',
                'arg2': 'value8',
                'arg3': 'value9',
            }
        }

        out_list = [out_header, out_lines]
        dict_list = [{
            'name': 'key1',
            'arg1': 'value1',
            'arg3': 'value3',
            'arg2': 'value2',
        }, {
            'name': 'key2',
            'arg1': 'value6',
            'arg2': 'value5',
            'arg3': 'value4',
        }, {
            'name': 'key3',
            'arg1': 'value7',
            'arg2': 'value8',
            'arg3': 'value9',
        }]

        from dyools import Data
        self.assertEqual(Data(dict_of_dict).get_header(), out_header)
        self.assertEqual(Data(dict_of_dict).get_lines(), out_lines)
        self.assertEqual(Data(dict_of_dict).to_list(), out_list)
        self.assertEqual(Data(dict_of_dict).to_dictlist(), dict_list)

    def test_data_list_of_values(self):
        in_header = ['Code', 'Name']
        in_values = ['MyCode', 'MyName']
        out_list = [in_header, [in_values]]
        out_dict = {
            'Name': 'MyName',
            'Code': 'MyCode',
        }
        out_dictlist = [out_dict]
        from dyools import Data
        self.assertEqual(Data(in_values, header=in_header).to_list(), out_list)
        self.assertEqual(Data(in_values, header=in_header).to_dictlist(), out_dictlist)
        self.assertEqual(in_header, Data(out_dictlist).get_header())
        self.assertEqual(in_header, Data(out_dictlist).get_header())
        self.assertEqual([in_values], Data(out_dictlist).get_lines())
        self.assertEqual(in_values, Data(out_dict).get_lines())

    def test_data_list_of_list(self):
        in_header = ['Name', 'Code']
        in_values = [['MyName1', 'MyCode1'], ['MyName2', 'MyCode2']]
        in_inline_values = [in_header, in_values[0], in_values[1]]
        out_list = [in_header, in_values]
        out_dict1 = {
            'Name': 'MyName1',
            'Code': 'MyCode1',
        }
        out_dict2 = {
            'Name': 'MyName2',
            'Code': 'MyCode2',
        }
        out_dictlist = [out_dict1, out_dict2]
        from dyools import Data
        self.assertEqual(Data(in_values, has_header=False).to_list(), [in_values])
        self.assertEqual(Data(out_list, has_header=True).to_dictlist(), out_dictlist)
        self.assertEqual(Data(in_inline_values, has_header=True).to_list(), out_list)
        self.assertEqual(Data(in_values, has_header=False).get_lines(), in_values)
        self.assertEqual(Data(in_values, has_header=False).get_header(), [0, 1])
        self.assertEqual(Data(in_values, header=in_header).to_list(), out_list)
        self.assertEqual(in_header, Data(in_inline_values, has_header=True).get_header())
        self.assertEqual(in_values, Data(in_inline_values, has_header=True).get_lines())

    def test_data_list_of_dict(self):
        in_header = ['Code', 'Name']
        in_values = [['MyCode1', 'MyName1'], ['MyCode2', 'MyName2']]
        out_list = [in_header, in_values]
        out_dict1 = {
            'Name': 'MyName1',
            'Code': 'MyCode1',
        }
        out_dict2 = {
            'Name': 'MyName2',
            'Code': 'MyCode2',
        }
        out_dictlist = [out_dict1, out_dict2]
        from dyools import Data
        self.assertEqual(Data(out_dict1, has_header=False).get_header(), in_header)
        self.assertEqual(Data(out_dict2, has_header=False).get_header(), in_header)
        self.assertEqual(Data(out_dictlist, has_header=False).get_header(), in_header)
        self.assertEqual(Data(out_dictlist, has_header=False).get_lines(), in_values)
        self.assertEqual(Data(out_dictlist, has_header=False).to_list(), out_list)
        self.assertEqual(Data(out_dictlist, has_header=True).to_list(), out_list)
        self.assertEqual(Data(out_list, has_header=True).to_dictlist(), out_dictlist)
