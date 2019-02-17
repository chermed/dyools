from unittest import TestCase


class TestDate(TestCase):
    def test_date_init(self):
        from dyools import Date
        self.assertEqual(Date("2019-10-10").to_str(), "2019-10-10")
        self.assertEqual(Date("2019-10-10").relativedelta(days=2), "2019-10-12")
        self.assertEqual(Date("2019-10-10").relativedelta(days=2, months=2), "2019-12-12")
        self.assertEqual(Date("2019-10-10").apply(days=2, months=2).to_str(), "2019-12-12")
        self.assertEqual(Date("2019-10-03").apply(days=2, months=2).to_fr(), "05/12/2019")
        self.assertEqual(Date("2019-10-10 12:12:12").to_str(), "2019-10-10 12:12:12")
        self.assertEqual(Date(2019, 10, 10, 12, 12, 12).to_str(), "2019-10-10 12:12:12")
        self.assertEqual(Date(2019, 10, 10).to_str(), "2019-10-10")
        self.assertEqual(Date(day=10, month=12, year=2000).to_str(), "2000-12-10")
        with self.assertRaises(Exception):
            Date(False)
        with self.assertRaises(Exception):
            Date(None)
        with self.assertRaises(Exception):
            Date(2019, 2)

    def test_date_operator(self):
        from dyools import Date
        self.assertEqual(Date("2019-10-03") + 10, "2019-10-13")
        self.assertEqual(Date("2019-10-03") - 1, "2019-10-02")
        self.assertEqual(Date("2019-10-03") + "-2d", "2019-10-01")
        self.assertEqual(Date("2019-10-03") + "+3d", "2019-10-06")
        self.assertEqual(Date("2019-10-03") + "1m", "2019-11-03")
        self.assertEqual(Date("2019-10-03") + "3y", "2022-10-03")
        self.assertEqual(type(Date("2019-10-03") + "3y"), type("2022-10-03"))

    def test_date_last_first_day(self):
        from dyools import Date
        self.assertEqual(Date("2019-10-03").last_day(), "2019-10-31")
        self.assertEqual(Date("2019-10-03").first_day(), "2019-10-01")

    def test_date_between(self):
        from dyools import Date
        d1 = "2019-02-20"
        d2 = "2019-02-21"
        d3 = "2019-02-22"
        self.assertTrue(Date(d2).is_between(False, d3))
        self.assertTrue(Date(d2).is_between(d1, False))
        self.assertTrue(Date(d2).is_between(d1, d3))
        self.assertTrue(Date(d2).is_between(d3, d1))
        self.assertTrue(Date(d1).is_between(d1, d3))
        self.assertTrue(Date(d3).is_between(d2, d3))
        self.assertTrue(Date(d2).is_between(False, d2))
        self.assertTrue(Date(d2).is_between(d2, False))
        self.assertFalse(Date(d3).is_between(False, d1))
        self.assertFalse(Date(d3).is_between(False, d2))
        self.assertFalse(Date(d3).is_between(d1, d2))
        self.assertFalse(Date(d2).is_between(d1, d1))
        self.assertFalse(Date(d2).is_between(False, d1))
