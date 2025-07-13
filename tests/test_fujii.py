import unittest
from fujii import fujii_scheduler
from common import Task

class TestFujiiScheduler(unittest.TestCase):
    def test_basic(self):
        tasks = {i: Task(i) for i in range(5)}
        precedence = {
            1: {3},
            2: {3},
            3: {4}
        }

        schedule = fujii_scheduler(tasks, precedence, m=2)
        scheduled_ids = [task.id for machine in schedule for task in machine]
        self.assertCountEqual(scheduled_ids, tasks.keys())

         # Проверка предшествования: для каждого u→v убедимся, что u завершилась до старта v
        for u, vs in precedence.items():
            for v in vs:
                self.assertLessEqual(tasks[u].end_time, tasks[v].start_time)
