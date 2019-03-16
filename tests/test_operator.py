from unittest import TestCase


class TestOperator(TestCase):
    def test_flat(self):
        from dyools import Operator
        origin = [[1, 2, (3, 4, 8)], [4, [5, 8], 6], [7], [8, 9, [[14]]]]
        result = [1, 2, 3, 4, 8, 4, 5, 8, 6, 7, 8, 9, 14]
        self.assertEqual(Operator.flat(origin), result)
        self.assertEqual(Operator.flat('TEST'), ['TEST'])
        self.assertEqual(Operator.flat(123), [123])
        self.assertEqual(Operator.flat(False), [False])
        origin = [[1, 3, 7], [False, True, None, 'Test'], [0]]
        result = [1, 3, 7, False, True, None, 'Test', 0]
        self.assertEqual(Operator.flat(*origin), result)
        self.assertEqual(Operator.flat(*result), result)
        self.assertEqual(Operator.flat(result), result)

    def test_split_and_flat(self):
        from dyools import Operator
        origin = ['sale,purchase', ['project', ('event', 'test,test')]]
        result = ['sale', 'purchase', 'project', 'event', 'test', 'test']
        self.assertEqual(Operator.split_and_flat(',', origin), result)
        self.assertEqual(Operator.split_and_flat(',', *origin), result)
        self.assertEqual(Operator.split_and_flat(',', result), result)
        self.assertEqual(Operator.split_and_flat(',', *result), result)
        self.assertEqual(Operator.split_and_flat(',', ('city',)), ['city'])

    def test_unique(self):
        from dyools import Operator
        origin = [1, 3, 1, False, 0, 0, None, 1, 8, 1, 9]
        result = [1, 3, False, 0, None, 8, 9]
        self.assertEqual(Operator.unique(origin), result)
        self.assertEqual(Operator.unique('test'), 'test')
        self.assertEqual(Operator.unique(1), 1)
        self.assertEqual(Operator.unique(['id', 'id', 'key', 'value']), ['id', 'key', 'value'])
        self.assertEqual(Operator.unique(['id', 'id']), ['id'])

    def test_intersection(self):
        from dyools import Operator
        self.assertEqual(Operator.intersection([1, 2, 3]), [1, 2, 3])
        self.assertEqual(Operator.intersection([], [1, 2, 3]), [])
        self.assertEqual(Operator.intersection([1, 2, 3], []), [])
        self.assertEqual(Operator.intersection([1, 2, 3], [3]), [3])
        self.assertEqual(Operator.intersection([1, 2, 3], [3, 2]), [2, 3])
        self.assertEqual(Operator.intersection([1, 2, 3], [3, 2], [2, 3], [3]), [3])
        self.assertEqual(Operator.intersection([0, 1, 2, 3, 0], [0, 3, 2, 0]), [0, 2, 3, 0])
        self.assertEqual(Operator.intersection(['id', 'name', 'id'], ['id', 'name']), ['id', 'name', 'id'])
        self.assertEqual(Operator.intersection(['id', 'key', 'value'], ['id']), ['id'])
        self.assertEqual(Operator.intersection(['id'], ['id', 'key', 'value']), ['id'])
        self.assertEqual(Operator.intersection(['id'], ['id', 'key', 'value'], ['A', 'id'], ['id']), ['id'])

    def test_unique_intersection(self):
        from dyools import Operator
        self.assertEqual(Operator.unique_intersection([], [1, 2, 3]), [])
        self.assertEqual(Operator.unique_intersection([1, 2, 3], []), [])
        self.assertEqual(Operator.unique_intersection([1, 2, 3], [3]), [3])
        self.assertEqual(Operator.unique_intersection([1, 2, 3], [3, 2]), [2, 3])
        self.assertEqual(Operator.unique_intersection([0, 1, 2, 3, 0], [0, 3, 2, 0]), [0, 2, 3])
        self.assertEqual(Operator.unique_intersection(['id', 'name'], ['id', 'name']), ['id', 'name'])
        self.assertEqual(Operator.unique_intersection(['id', 'key', 'value'], ['id']), ['id'])
        self.assertEqual(Operator.unique_intersection(['id'], ['id', 'key', 'value']), ['id'])
