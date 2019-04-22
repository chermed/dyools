from unittest import TestCase


class TestTool(TestCase):
    def test_protecting_dict(self):
        from dyools import Tool
        data = {'a': 10, 2: 20}
        data_copy = data.copy()
        data_diff = {'a': 30, 2: 20}
        with Tool.protecting_items(data, ['a', 2]):
            data['a'] = 30
            self.assertEqual(data, data_diff)
        self.assertEqual(data, data_copy)

    def test_protecting_list(self):
        from dyools import Tool
        data = ['a', 10, 2, 20]
        data_copy = data[:]
        data_diff = ['a', 30, 2, 20]
        with Tool.protecting_items(data, [1]):
            data[1] = 30
            self.assertEqual(data, data_diff)
        self.assertEqual(data, data_copy)

    def test_protecting_object(self):
        class klass_obj(object):
            def __init__(self, a, b):
                self.a = a
                self.b = b

        from dyools import Tool
        obj = klass_obj(10, 20)
        obj_copy = klass_obj(10, 20)
        obj_diff = klass_obj(10, 30)
        with Tool.protecting_attributes(obj, ['b', 'a']):
            obj.b = 30
            self.assertEqual(obj.b, obj_diff.b)
            self.assertEqual(obj.a, obj_copy.a)
        self.assertEqual(obj.a, obj_copy.a)
        self.assertEqual(obj.b, obj_copy.b)

    def test_construct_domain_from_str(self):
        from dyools import Tool
        c = Tool.construct_domain_from_str
        self.assertEqual(c('a = 1'), [('a', '=', 1)])
        self.assertEqual(c('a = M'), [('a', '=', 'M')])
        self.assertEqual(c('a = "M+"'), [('a', '=', 'M+')])
        self.assertEqual(c('a = "2+2"'), [('a', '=', '2+2')])
        self.assertEqual(c('a = 1 and b == 4'), ['&', ('a', '=', 1), ('b', '=', 4)])
        self.assertEqual(c('a = 1 or b == 4'), ['|', ('a', '=', 1), ('b', '=', 4)])
        self.assertEqual(c("a = '1' or b == 4"), ['|', ('a', '=', '1'), ('b', '=', 4)])
