from unittest import TestCase


class TestOffsetLimit(TestCase):
    def test_offset_limit(self):
        from dyools import OffsetLimit
        s1 = OffsetLimit(0, 2, 7)
        res1 = [[0, 2], [2, 2], [4, 2], [6, 1]]
        s2 = OffsetLimit(0, 2, 3)
        res2 = [[0, 2], [2, 1]]
        s3 = OffsetLimit(0, 2, 2)
        res3 = [[0, 2]]
        s4 = OffsetLimit(0, 2, 8)
        res4 = [[0, 2], [2, 2], [4, 2], [6, 2]]
        self.assertEqual(list(s1), res1)
        self.assertEqual(list(s2), res2)
        self.assertEqual(list(s3), res3)
        self.assertEqual(list(s4), res4)
