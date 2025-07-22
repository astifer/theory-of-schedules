import unittest
from gabow import gabow_scc
from common import get_graph

class TestGabowSCC(unittest.TestCase):
    def test_scc_detection(self):
        # Простой цикл 1→2→3→1
        precedence = {
            1: {2},
            2: {3},
            3: {1},
            4: set()
        }
        succ, _ = get_graph(precedence)
        components = gabow_scc(succ)
        # Должен найти один компонент длины 3
        self.assertTrue(any(set(comp) == {1,2,3} for comp in components))

    def test_acyclic(self):
        # Линейный DAG 1←2←3←4, никакие циклы
        precedence = {
            1: set(),
            2: {1},
            3: {2},
            4: {3}
        }
        succ, _ = get_graph(precedence)
        components = gabow_scc(succ)
        # Все компоненты по одному элементу
        self.assertTrue(all(len(comp) == 1 for comp in components))
        # Должно содержать ровно эти вершины
        found = {next(iter(comp)) for comp in components}
        self.assertEqual(found, {1,2,3,4})

    def test_multiple_scc(self):
        # Две отдельные циклические компоненты и один изолят
        precedence = {
            1: {2},
            2: {1},
            3: {4},
            4: {3},
            5: set()
        }
        succ, _ = get_graph(precedence)
        components = gabow_scc(succ)
        # Ожидаем SCC: {1,2}, {3,4}, {5}
        comp_sets = [set(comp) for comp in components]
        self.assertIn({1,2}, comp_sets)
        self.assertIn({3,4}, comp_sets)
        self.assertIn({5}, comp_sets)
        self.assertEqual(len(comp_sets), 3)

    def test_single_node_self_loop(self):
        # Самопетля считается SCC из одного узла
        precedence = {
            1: {1},  # хотя граф цикличен, алгоритм выделит 1 как SCC
            2: set()
        }
        succ, _ = get_graph(precedence)
        components = gabow_scc(succ)
        comp_sets = [set(comp) for comp in components]
        self.assertIn({1}, comp_sets)
        self.assertIn({2}, comp_sets)
        self.assertEqual(len(comp_sets), 2)

    def test_large_cycle(self):
        # Большой цикл из 5 узлов
        n = 5
        precedence = {i: {(i % n) + 1} for i in range(1, n+1)}
        succ, _ = get_graph(precedence)
        components = gabow_scc(succ)
        # Единственный SCC всех пяти узлов
        comp_sets = [set(comp) for comp in components]
        self.assertEqual(len(comp_sets), 1)
        self.assertEqual(comp_sets[0], set(range(1, n+1)))

if __name__ == "__main__":
    unittest.main()
