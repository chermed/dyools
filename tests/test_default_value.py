from unittest import TestCase


class TestDefaultValue(TestCase):

    def test_get_item(self):
        m = [1, False, None, 0]
        from dyools import DefaultValue
        dv_m1 = DefaultValue(m)
        dv_m2 = DefaultValue(m, {})
        self.assertEqual(dv_m1[0], 1)
        self.assertEqual(dv_m1[1], '')
        self.assertEqual(dv_m1[2], '')
        self.assertEqual(dv_m1[3], 0)
        self.assertEqual(dv_m2[0], 1)
        self.assertEqual(dv_m2[1], False)
        self.assertEqual(dv_m2[2], None)
        self.assertEqual(dv_m2[3], 0)

    def test_get_attr(self):
        class m(object):
            def __init__(self, a, b):
                self.a = a
                self.b = b

        m1 = m(False, None)
        m2 = m(False, None)
        from dyools import DefaultValue
        dv_m1 = DefaultValue(m1)
        dv_m2 = DefaultValue(m2, {})
        self.assertEqual(dv_m1.a, '')
        self.assertEqual(dv_m1.b, '')
        self.assertEqual(dv_m2.a, False)
        self.assertEqual(dv_m2.b, None)

    def test_get_attr_type(self):
        class m(object):
            def __init__(self, a, b):
                self.a = a
                self.b = b

        m1 = m(False, None)
        m2 = m(False, None)
        m2.sub = m1
        from dyools import DefaultValue
        dv_m = DefaultValue(m2, types=(m,))
        print(dv_m.sub)
        self.assertEqual(dv_m.sub.a, '')
