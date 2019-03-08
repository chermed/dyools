from unittest import TestCase


class TestStr(TestCase):
    def test_str(self):
        from dyools import Str
        self.assertEqual(Str(' a éçè %345 hy ').to_code(), "A_ECE_345_HY")
        self.assertEqual(Str('       ').to_code(), '')
        self.assertEqual(Str('   e    ').to_code(), 'E')
        self.assertEqual(Str([1, 5, 8]).to_str().replace(' ', ''), '[1,5,8]')
        self.assertEqual(Str(' de texté ').remove_spaces(), 'detexté')
        self.assertEqual(Str(' de texté ').remove_accents(), ' de texte ')

    def test_str_combinations(self):
        from dyools import Str
        self.assertEqual(sorted(Str('*.py').case_combinations()), sorted(['*.py', '*.Py', '*.pY', '*.PY']))

