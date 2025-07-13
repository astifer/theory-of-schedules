import unittest
from gabow import gabow_scc
from common import get_graph

class TestGabowSCC(unittest.TestCase):
    def test_scc_detection(self):
        precedence = {
            1: {2},
            2: {3},
            3: {1},  # цикл
            4: set()
        }
        succ, _ = get_graph(precedence)
        components = gabow_scc(succ)

        has_cycle = any(len(comp) > 1 for comp in components)
        self.assertTrue(has_cycle)

    def test_acyclic(self):
        precedence = {
            1: set(),
            2: {1},
            3: {2},
            4: {3}
        }
        succ, _ = get_graph(precedence)
        components = gabow_scc(succ)

        for comp in components:
            self.assertEqual(len(comp), 1)
