import unittest
from fujii import fujii_scheduler
from common import Task

class TestFujiiScheduler(unittest.TestCase):
    def test_basic_dependency(self):
        """
        Простой граф с зависимостями:
        1→3, 2→3, 3→4
        """
        tasks = {i: Task(i, duration=1) for i in range(1, 5)}
        precedence = {
            1: {3},
            2: {3},
            3: {4},
            4: set()
        }
        schedule = fujii_scheduler(tasks, precedence, m=2)
        self._check_functional(tasks, precedence, schedule, m=2)

    def test_no_dependencies_concurrency(self):
        """
        Без зависимостей. Проверяем, что одновременно 
        выполняется не более m задач.
        """
        n = 10
        m = 3
        tasks = {i: Task(i, duration=(i % 3) + 1) for i in range(1, n+1)}
        precedence = {i: set() for i in tasks}
        schedule = fujii_scheduler(tasks, precedence, m=m)
        self._check_functional(tasks, precedence, schedule, m=m)

        # Проверяем глобальную нагрузку
        events = []
        for machine in schedule:
            for t in machine:
                events.append((t.start_time, +1))
                events.append((t.end_time, -1))
        active = 0
        for time, delta in sorted(events):
            active += delta
            self.assertLessEqual(active, m)

    def test_chain_parallel(self):
        """
        Простая цепочка 1→2→3→4→5 с двухмашинным параллелизмом.
        Должно выдержать зависимости.
        """
        tasks = {i: Task(i, duration=1) for i in range(1, 6)}
        precedence = {i: {i-1} for i in range(2, 6)}
        precedence[1] = set()
        schedule = fujii_scheduler(tasks, precedence, m=2)
        self._check_functional(tasks, precedence, schedule, m=2)

    def test_complex_structure(self):
        """
        Сложный граф без строгих makespan-проверок:
                  1
                 / \
                2   3
                |   |
                4   5
                 \ /
                  6
        """
        tasks = {i: Task(i, duration=(i % 2) + 1) for i in range(1, 7)}
        precedence = {
            1: set(),
            2: {1},
            3: {1},
            4: {2},
            5: {3},
            6: {4, 5},
        }
        schedule = fujii_scheduler(tasks, precedence, m=2)
        self._check_functional(tasks, precedence, schedule, m=2)

    def _check_functional(self, tasks, precedence, schedule, m):
        # 1. Все задачи назначены ровно один раз
        assigned = [t.id for machine in schedule for t in machine]
        self.assertCountEqual(assigned, tasks.keys())

        # 2. Нет перекрытий на каждой машине
        for machine in schedule:
            machine.sort(key=lambda t: t.start_time)
            for a, b in zip(machine, machine[1:]):
                self.assertLessEqual(a.end_time, b.start_time)

        # 3. Соблюдение зависимостей
        for u, vs in precedence.items():
            for v in vs:
                self.assertLessEqual(tasks[u].end_time, tasks[v].start_time)

        # 4. Одновременная загрузка ≤ m
        events = []
        for machine in schedule:
            for t in machine:
                events.append((t.start_time, +1))
                events.append((t.end_time, -1))
        active = 0
        for time, delta in sorted(events):
            active += delta
            self.assertLessEqual(active, m)


if __name__ == "__main__":
    unittest.main()
