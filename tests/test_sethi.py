import unittest
from sethi import sethi_ulman_schedule
from common import Task, get_graph

class TestSethiUllman(unittest.TestCase):
    def test_simple_chain(self):
        # Простая цепочка 1→2→3→4
        precedence = {
            1: set(),
            2: {1},
            3: {2},
            4: {3}
        }
        succ, pred = get_graph(precedence)
        order = sethi_ulman_schedule(succ, pred)
        # Должен быть [1,2,3,4]
        self.assertEqual(order, [1,2,3,4])

    def test_parallel_leaves(self):
        # Две независимые ветки, потом объединяются
        #    1   2
        #     \ /
        #      3
        precedence = {
            1: set(),
            2: set(),
            3: {1,2}
        }
        succ, pred = get_graph(precedence)
        order = sethi_ulman_schedule(succ, pred)
        # Первые два могут стоять в любом порядке, но перед 3
        self.assertIn(order[0], [1,2])
        self.assertIn(order[1], [1,2])
        self.assertNotEqual(order[0], order[1])
        self.assertEqual(order[2], 3)

    def test_diamond(self):
        # Ромб 1→(2,3)→4
        precedence = {
            1: set(),
            2: {1},
            3: {1},
            4: {2,3}
        }
        succ, pred = get_graph(precedence)
        order = sethi_ulman_schedule(succ, pred)
        # 1 first, 4 last, 2 and 3 in middle (any order)
        self.assertEqual(order[0], 1)
        self.assertEqual(order[3], 4)
        self.assertCountEqual(order[1:3], [2,3])

    def test_complex_dag(self):
        # Более сложный DAG
        precedence = {
            1: set(),
            2: {1},
            3: {1},
            4: {2},
            5: {2},
            6: {3,4},
            7: {5},
            8: {6,7}
        }
        succ, pred = get_graph(precedence)
        order = sethi_ulman_schedule(succ, pred)
        # Проверка топологического порядка
        pos = {v:i for i,v in enumerate(order)}
        for u, vs in precedence.items():
            for v in vs:
                self.assertLess(pos[v], pos[u])

    def test_cycle_detection(self):
        # Цикл 1→2→1 должен вызвать исключение
        precedence = {
            1: {2},
            2: {1}
        }
        succ, pred = get_graph(precedence)
        with self.assertRaises(ValueError):
            sethi_ulman_schedule(succ, pred)

    def test_single_node(self):
        # Одиночная задача без связей
        precedence = {1: set()}
        succ, pred = get_graph(precedence)
        order = sethi_ulman_schedule(succ, pred)
        self.assertEqual(order, [1])
    
    def test_single_node(self):
        # Одиночная задача без связей
        precedence = {1: set()}
        succ, pred = get_graph(precedence)
        order = sethi_ulman_schedule(succ, pred)
        self.assertEqual(order, [1])

    def test_long_chain(self):
        """
        Длинная цепочка из 20 узлов: 1→2→3→...→20
        Проверяем, что порядок именно 1,2,...,20
        """
        n = 20
        precedence = {i: {i-1} for i in range(2, n+1)}
        precedence[1] = set()
        succ, pred = get_graph(precedence)
        order = sethi_ulman_schedule(succ, pred)
        # Ожидаем ровно последовательность 1..20
        self.assertEqual(order, list(range(1, n+1)))

if __name__ == '__main__':
    unittest.main()
