import unittest
from sethi import sethi_ulman_schedule
from common import Task, get_graph

class TestSethiUllman(unittest.TestCase):
    def test_topological_order(self):
        precedence = {
            1: set(),
            2: set(),
            3: {1, 2},
            4: {3}
        }
        succ, pred = get_graph(precedence)
        order = sethi_ulman_schedule(succ, pred)

        # Проверка топологического порядка
        position = {task_id: i for i, task_id in enumerate(order)}
        for task, preds in precedence.items():
            for pred in preds:
                self.assertLess(position[pred], position[task])
