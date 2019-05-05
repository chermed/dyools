from unittest import TestCase


class TestSlice(TestCase):
    def test_slice(self):
        from dyools import Slice
        data = [1, 2, 3, 4, 5]
        s1 = Slice(data, 1)
        res1 = [[x] for x in data]
        s2 = Slice(data, 2)
        res2 = [[1, 2], [3, 4], [5]]
        s3 = Slice(data, 3)
        res3 = [[1, 2, 3], [4, 5]]
        self.assertEqual(list(s1.get()), res1)
        self.assertEqual(list(s2.get()), res2)
        self.assertEqual(list(s3.get()), res3)
