from unittest import TestCase


class TestConvert(TestCase):
    def test_convert_data(self):
        from dyools import Convert
        self.assertEqual(Convert.data(1024*1024, origin='b', to='mb'), 1)
        self.assertEqual(Convert.data(1024, origin='kb', to='mb'), 1)
        self.assertEqual(Convert.data(1024, origin='mb', to='gb'), 1)
        self.assertEqual(Convert.data(2048, origin='mb', to='gb'), 2)
        self.assertEqual(Convert.data(2048, origin='mb', to='gb'), 2)
        self.assertEqual(Convert.data(1048576, origin='mb', to='gb'), 1024)
        self.assertEqual(Convert.data(12582912, origin='kb', to='gb'), 12)
