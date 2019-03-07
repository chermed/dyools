from unittest import TestCase


class TestIS(TestCase):
    def test_is_str(self):
        from dyools import IS
        self.assertTrue(IS.str('Text'))
        self.assertTrue(IS.str(''))
        self.assertFalse(IS.str(3))

    def test_is_empty(self):
        from dyools import IS
        self.assertTrue(IS.empty([]))
        self.assertTrue(IS.empty(''))
        self.assertTrue(IS.empty({}))
        self.assertTrue(IS.empty(' '))
        self.assertFalse(IS.empty(' test'))

    def test_is_xmlid(self):
        from dyools import IS
        self.assertTrue(IS.xmlid('test.test'))
        self.assertTrue(IS.xmlid('1234_abdcd.1234_abdcd'))
        self.assertTrue(IS.xmlid('1234.1234'))
        self.assertTrue(IS.xmlid('abcd.abcd'))
        self.assertTrue(IS.xmlid('____.___'))
        self.assertFalse(IS.xmlid('.'))
        self.assertFalse(IS.xmlid('ab cd.efgh'))
        self.assertFalse(IS.xmlid('---.---'))
        self.assertFalse(IS.xmlid('ABCD.EFGH'))
        self.assertFalse(IS.xmlid(' '))
        self.assertFalse(IS.xmlid(6))
        self.assertFalse(IS.xmlid([]))
        self.assertFalse(IS.xmlid('abcd'))

    def test_is_domain(self):
        from dyools import IS
        self.assertTrue(IS.domain([]))
        self.assertTrue(IS.domain([('x', '=', 'Y')]))
        self.assertTrue(IS.domain([('x', '=', 'Y'), ('x', '=', 'Y')]))
        self.assertTrue(IS.domain(['&', '|', ('x', '=', 'Y'), ('x', '=', 'Y'), ('x', '=', 'Y')]))
        self.assertTrue(IS.domain([('x', '=', 100)]))
        self.assertFalse(IS.domain(''))
        self.assertFalse(IS.domain('text'))
        self.assertFalse(IS.domain(False))
        self.assertFalse(IS.domain(None))
        self.assertFalse(IS.domain(['f']))
        self.assertFalse(IS.domain([(6, 0, [])]))
        self.assertFalse(IS.domain([(0, 0, {})]))
        self.assertFalse(IS.domain(['&']))
        self.assertFalse(IS.domain(['x', '=', 5]))


    def test_is_iterable(self):
        from dyools import IS
        self.assertTrue(IS.iterable([]))
        self.assertTrue(IS.iterable([1, 2, 3, 4]))
        self.assertTrue(IS.iterable(()))
        self.assertTrue(IS.iterable((1, 2, 3, 4,)))
        self.assertTrue(IS.iterable({}))
        self.assertTrue(IS.iterable({'a': 1}))
        self.assertFalse(IS.iterable(''))
        self.assertFalse(IS.iterable('abcdefgh'))
        self.assertFalse(IS.iterable(1234))
