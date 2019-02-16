from unittest import TestCase


class TestEval(TestCase):
    def test_eval(self):
        from dyools import Eval
        ctx = {
            'a': 5,
            'b': 90
        }
        item = {
            'z': '{a}'
        }
        res = {
            'z': 5
        }
        self.assertEqual(Eval(item, ctx).eval(), res)

    def test_eval_2(self):
        from dyools import Eval
        ctx = {
            'fname': 'Med',
        }
        item = [['$fname$', 'Maroc'], ['$fname$', 'Maroc']]
        res = [['Med', 'Maroc'], ['Med', 'Maroc']]
        self.assertEqual(Eval(item, ctx).eval(), res)
