import sys
from datetime import datetime
from unittest import TestCase


class TestXML(TestCase):
    def setUp(self):
        pass

    def test_sequence_int(self):
        from dyools import Sequence
        s = Sequence()
        self.assertEqual(s.value, 1)
        self.assertEqual(s.next(), 2)
        self.assertEqual(s.next(), 3)
        self.assertEqual(s.value, 3)

    def test_sequence_str_with_int(self):
        from dyools import Sequence
        s = Sequence(start=4, padding=3, prefix='PRE', suffix='END')
        self.assertEqual(s.value, 'PRE004END')
        self.assertEqual(s.next(), 'PRE005END')
        self.assertEqual(s.value, 'PRE005END')

    def test_sequence_int_with_step(self):
        from dyools import Sequence
        s = Sequence(start=0, step=10)
        self.assertEqual(s.value, 0)
        self.assertEqual(s.next(), 10)
        self.assertEqual(s.next(), 20)
        self.assertEqual(s.value, 20)

    def test_sequence_char(self):
        from dyools import Sequence
        s = Sequence(start='x')
        self.assertEqual(s.value, 'x')
        self.assertEqual(s.next(), 'y')
        self.assertEqual(s.next(), 'z')
        self.assertEqual(s.next(), 'aa')
        self.assertEqual(s.next(), 'ab')
        self.assertEqual(s.next(), 'ac')
        self.assertEqual(s.value, 'ac')


    def test_sequence_date_year(self):
        from dyools import Sequence
        date = datetime.now()
        res = '{}0001{:0>2}'.format(date.year, date.day)
        s = Sequence(start=1, padding=4, prefix='%(year)s', suffix='%(day)s', prefix_padding=2, suffix_padding=2)
        self.assertEqual(s.value, res)



