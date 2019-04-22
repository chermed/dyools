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

    def test_dot_to_underscore(self):
        from dyools import Str
        self.assertEqual(Str('__name').dot_to_underscore(), '__name')
        self.assertEqual(Str('__name.x').dot_to_underscore(), '__name_x')
        self.assertEqual(Str('__name.last').dot_to_underscore(), '__name_last')
        self.assertEqual(Str('__name_LAST').dot_to_underscore(), '__name_LAST')
        self.assertEqual(Str('__name_LAST___').dot_to_underscore(), '__name_LAST___')

    def test_get_number(self):
        from dyools import Str
        self.assertEqual(Str('_34_89__78__.__78').to_number(), 348978.78)
        self.assertEqual(Str('_34e_89_e_78__._g_78').to_number(), 348978.78)
        self.assertEqual(Str('_34e_89_e_78__._8g_78').get_first_number(), 34)
        self.assertEqual(Str('_3.4e_89_e_78__._8g_78').get_first_number(), 3.4)
        self.assertEqual(Str('_34e_89_e_78__._8g_78').get_last_number(), 78)
        self.assertEqual(Str('_34e_89_e_78__._8g_7,8').get_last_number(), 7.8)

    def test_to_range(self):
        from dyools import Str
        self.assertEqual(Str('  9 ').to_range(ttype=int), (9, 9))
        self.assertEqual(Str('>80').to_range(ttype=int), (81, 99999))
        self.assertEqual(Str('>80').to_range(), (80.01, 99999))
        self.assertEqual(Str('>=80').to_range(), (80, 99999))
        self.assertEqual(Str('<80').to_range(ttype=float), (0, 79.99))
        self.assertEqual(Str('<80').to_range(ttype=int), (0, 79))
        self.assertEqual(Str('<80').to_range(ttype=int, or_equal=True), (0, 80))
        self.assertEqual(Str(' weignt < 80 kg').to_range(ttype=int, or_equal=True), (0, 80))
        self.assertEqual(Str('<=80').to_range(), (0, 80))
        self.assertEqual(Str('  3 - 78').to_range(), (3, 78))
        self.assertEqual(Str('  3,8 - 78').to_range(), (3.8, 78))
        self.assertEqual(Str('  3.8 - 78').to_range(), (3.8, 78))
        self.assertEqual(Str('  3.8 mm - 78kg ').to_range(), (3.8, 78))
        self.assertEqual(Str('  3.8  78').to_range(separators=[' ']), (3.8, 78))
        self.assertEqual(Str('  3.8 * 7.8   ').to_range(separators=['*']), (3.8, 7.8))
        self.assertEqual(Str('  30 * 23   ').to_range(separators=['*']), (23, 30))
        self.assertEqual(Str('  23 * 30   ').to_range(separators=['*']), (23, 30))
        self.assertEqual(Str(' test weight 23.5 kg * 30.kg distance   ').to_range(separators=['*']), (23.5, 30))
        self.assertEqual(Str(' test weight 23.5 kg * 30.kg distance   ').to_range(separators=['*'], ttype=int),
                         (23, 30))
        self.assertEqual(Str('>=80').to_range(max_number=99), (80, 99))
        self.assertEqual(Str('<=80').to_range(min_number=10), (10, 80))
