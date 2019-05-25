from unittest import TestCase


class TestPath(TestCase):
    def test_path_join(self):
        from dyools import Path
        paths = ['a1', 'a2', 'a3', 'a4']
        out = 'a1/a2/a3/a4'
        self.assertEqual(out, Path.join(paths))
        self.assertEqual(out, Path.join(*paths))

