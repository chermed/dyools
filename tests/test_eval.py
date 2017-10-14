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
