from unittest import TestCase


class TestEval(TestCase):
    def test_eval_dict_1(self):
        from dyools import Eval
        ctx = {'a': 5, 'b': 90}
        item = {'z': '{a}'}
        res = {'z': 5}
        self.assertEqual(Eval(item, ctx).eval(), res)

    def test_eval_dict_1(self):
        from dyools import Eval
        ctx = {'a': 5, 'b': 90, 'z': 'Z'}
        item = {
            '{a}': '{b}',
            '{b}': ['{z}', '{z}']
        }
        res = {5: 90, 90: ['Z', 'Z']}
        self.assertEqual(Eval(item, ctx).eval(), res)

    def test_eval_list_1(self):
        from dyools import Eval
        ctx = {'fname': 'dupont','a': 5, }
        item = [['{fname}', 'TEST'], ['{fname}', [[[['{a}']]]]]]
        res_int = [['dupont', 'TEST'], ['dupont', [[[[5]]]]]]
        res_str = [['dupont', 'TEST'], ['dupont', [[[['5']]]]]]
        self.assertEqual(Eval(item, ctx).eval(eval_result=True), res_int)
        self.assertEqual(Eval(item, ctx).eval(eval_result=False), res_str)

    def test_eval_list_2(self):
        from dyools import Eval
        ctx = {'fname': 'Dupont', }
        item = [['{fname}', 'Country'], ['{fname}', 'Country']]
        res = [['Dupont', 'Country'], ['Dupont', 'Country']]
        self.assertEqual(Eval(item, ctx).eval(), res)
