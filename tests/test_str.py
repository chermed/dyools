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

    def test_with_separator(self):
        from dyools import Str
        self.assertEqual(Str(12000000).numeric, True)
        self.assertEqual(Str('567').numeric, False)
        self.assertEqual(Str('567', numeric=True).numeric, True)
        self.assertEqual(Str(12000000).with_separator(), '12 000 000')
        self.assertEqual(Str(12000000.49).with_separator(), '12 000 000.49')
        self.assertEqual(Str(12000000.00).with_separator(), '12 000 000.00')
        self.assertEqual(Str(12000000.0000, precision=4).with_separator(), '12 000 000.0000')
        self.assertEqual(Str(12000000.0000, precision=6).with_separator(), '12 000 000.000000')
        self.assertEqual(Str(12000000.3, precision=6).with_separator(), '12 000 000.300000')
        self.assertEqual(Str(2).with_separator(), '2')
        self.assertEqual(Str('1367').with_separator(), '1 367')
        self.assertEqual(Str('1234567890').with_separator(sep=''), '1234567890')
        self.assertEqual(Str('1234567890').with_separator(sep='-'), '1-234-567-890')
        self.assertEqual(Str('1234567890').with_separator(sep='-', rtl=False), '123-456-789-0')
        self.assertEqual(Str('1367', numeric=True).with_separator(), '1 367')

    def test_replace(self):
        from dyools import Str
        s = Str('éçàèé').replace(dict(
            e=['é', 'è', 'ê'],
            c='ç',
            a=['à', 'â'],
        ))
        self.assertEqual(s, 'ecaee')

    def test_to_title(self):
        from dyools import Str
        self.assertEqual(Str('__name').to_title(), 'Name')
        self.assertEqual(Str('__name.x').to_title(), 'Name X')
        self.assertEqual(Str('__name.last').to_title(), 'Name Last')
        self.assertEqual(Str('__name_LAST').to_title(), 'Name Last')
        self.assertEqual(Str('__name_LAST___').to_title(), 'Name Last')
