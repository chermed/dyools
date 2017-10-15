from unittest import TestCase


class TestIF(TestCase):
    def test_is_str(self):
        from dyools import IF
        self.assertTrue(IF.is_str('Text'))
        self.assertTrue(IF.is_str(''))
        self.assertFalse(IF.is_str(3))

    def test_is_empty(self):
        from dyools import IF
        self.assertTrue(IF.is_empty([]))
        self.assertTrue(IF.is_empty(''))
        self.assertTrue(IF.is_empty({}))
        self.assertTrue(IF.is_empty(' '))
        self.assertFalse(IF.is_empty(' test'))

    def test_is_xmlid(self):
        from dyools import IF
        self.assertTrue(IF.is_xmlid('test.test'))
        self.assertTrue(IF.is_xmlid('1234_abdcd.1234_abdcd'))
        self.assertTrue(IF.is_xmlid('1234.1234'))
        self.assertTrue(IF.is_xmlid('abcd.abcd'))
        self.assertTrue(IF.is_xmlid('____.___'))
        self.assertFalse(IF.is_xmlid('.'))
        self.assertFalse(IF.is_xmlid('ab cd.efgh'))
        self.assertFalse(IF.is_xmlid('---.---'))
        self.assertFalse(IF.is_xmlid('ABCD.EFGH'))
        self.assertFalse(IF.is_xmlid(' '))
        self.assertFalse(IF.is_xmlid(6))
        self.assertFalse(IF.is_xmlid([]))

    def test_is_iterable(self):
        from dyools import IF
        self.assertTrue(IF.is_iterable([]))
        self.assertTrue(IF.is_iterable([1, 2, 3, 4]))
        self.assertTrue(IF.is_iterable(()))
        self.assertTrue(IF.is_iterable((1, 2, 3, 4,)))
        self.assertTrue(IF.is_iterable({}))
        self.assertTrue(IF.is_iterable({'a': 1}))
        self.assertFalse(IF.is_iterable(''))
        self.assertFalse(IF.is_iterable('abcdefgh'))
        self.assertFalse(IF.is_iterable(1234))
