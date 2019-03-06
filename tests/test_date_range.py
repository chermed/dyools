from unittest import TestCase


class TestDateRange(TestCase):
    def test_date_range(self):
        from dyools import Date
        begin = list(Date.date_range("2019-01-03", "2019-01-05"))
        res = ["2019-01-03", "2019-01-04","2019-01-05"]
        self.assertEqual(begin, res)

