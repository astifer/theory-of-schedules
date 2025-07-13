import unittest
from coffman import coffman_graham
from common import Task

class TestCoffmanGraham(unittest.TestCase):
    def test_simple_schedule(self):
        tasks = {i: Task(i) for i in range(1, 6)}
        precedence = {
            1: {3},
            2: {3},
            3: {4},
            4: {5}
        }
        schedule = coffman_graham(tasks, precedence, m=2)

        # Проверим, что все задачи назначены
        scheduled_tasks = [task.id for machine in schedule for task in machine]
        self.assertCountEqual(scheduled_tasks, tasks.keys())

        # Проверим, что нет конфликтов
        for machine in schedule:
            machine.sort(key=lambda t: t.start_time)
            for i in range(len(machine) - 1):
                self.assertLessEqual(machine[i].end_time, machine[i+1].start_time)

        # Проверим предшествование: для каждого u→v убедимся, что u завершилась до старта v
        for u, vs in precedence.items():
            for v in vs:
                self.assertLessEqual(tasks[u].end_time, tasks[v].start_time)

