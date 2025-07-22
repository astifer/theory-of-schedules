import unittest
from coffman import coffman_graham
from common import Task

class TestCoffmanGraham(unittest.TestCase):
    def test_simple_schedule(self):
        # Базовый пример с цепочкой зависимостей
        tasks = {i: Task(i) for i in range(1, 6)}
        precedence = {
            1: {3},
            2: {3},
            3: {4},
            4: {5}
        }
        schedule = coffman_graham(tasks, precedence, m=2)
        self._check_schedule(tasks, precedence, schedule)

    def test_no_dependencies(self):
        # Все задачи независимы: должно выровняться по машинам почти поровну
        n = 7
        tasks = {i: Task(i, duration=1) for i in range(1, n+1)}
        precedence = {i: set() for i in tasks}
        schedule = coffman_graham(tasks, precedence, m=3)
        self._check_schedule(tasks, precedence, schedule)

        # Проверяем балансировку: ни одна машина не должна получить больше ceil(n/m) и меньше floor(n/m)
        sizes = [len(machine) for machine in schedule]
        self.assertTrue(all(size in (n//3, n//3 + 1) for size in sizes))

    def test_long_chain(self):
        # Цепочка из 5 задач: 1→2→3→4→5
        tasks = {i: Task(i, duration=i) for i in range(1, 6)}
        precedence = {i: {i-1} for i in range(2, 6)}
        precedence[1] = set()
        schedule = coffman_graham(tasks, precedence, m=2)
        self._check_schedule(tasks, precedence, schedule)

        # Проверяем, что каждая следующая стартует ровно после окончания предыдущей
        order = [task for machine in schedule for task in machine]
        order.sort(key=lambda t: t.start_time)
        for prev, curr in zip(order, order[1:]):
            self.assertGreaterEqual(curr.start_time, prev.end_time)

    def test_complex_graph(self):
        # Более сложный граф зависимостей
        tasks = {i: Task(i) for i in range(1, 11)}
        precedence = {
            1: set(),
            2: {1},
            3: {1},
            4: {2, 3},
            5: {2},
            6: {3},
            7: {4, 5},
            8: {5, 6},
            9: {7, 8},
            10: {9}
        }
        schedule = coffman_graham(tasks, precedence, m=3)
        self._check_schedule(tasks, precedence, schedule)

        # Проверим makespan: не больше суммы самых длинных по цепочке
        longest_chain = sum(tasks[i].duration for i in [1, 2, 4, 7, 9, 10])
        makespan = max(task.end_time for machine in schedule for task in machine)
        self.assertLessEqual(makespan, longest_chain)

    def _check_schedule(self, tasks, precedence, schedule):
        # Все задачи назначены ровно один раз
        scheduled = [t.id for machine in schedule for t in machine]
        self.assertCountEqual(scheduled, tasks.keys())

        # На каждой машине нет перекрытий
        for machine in schedule:
            machine.sort(key=lambda t: t.start_time)
            for a, b in zip(machine, machine[1:]):
                self.assertLessEqual(a.end_time, b.start_time)

        # Зависимости соблюдены
        for u, vs in precedence.items():
            for v in vs:
                self.assertLessEqual(tasks[u].end_time, tasks[v].start_time)

if __name__ == '__main__':
    unittest.main()
