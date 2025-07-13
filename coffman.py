from collections import defaultdict, deque
import heapq
from typing import List

from common import Task, get_graph

def coffman_graham(tasks: List[Task], precedence, m=2):
    """
    Реализация алгоритма Coffman-Graham.
    tasks: dict[int, Task] — задачи
    precedence: dict[int, set[int]] — предшествование (ребро i -> j: i предшествует j)
    m: число машин
    """
    
    succ, pred = get_graph(precedence)
    for t in tasks:
        succ.setdefault(t, set())
        pred.setdefault(t, set())
        
    # dычисляем топологическую сортировку с присвоением меток
    def compute_labels():
        in_degree = {t: len(pred[t]) for t in tasks}
        queue = [t for t in tasks if in_degree[t] == 0]
        labels = dict()
        step = 1
        while queue:
            queue.sort(reverse=True) 
            t = queue.pop()
            labels[t] = step
            step += 1
            for v in succ[t]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
        return labels

    labels = compute_labels()

    # сортировка задач по возрастанию меток
    ordered_tasks = sorted(tasks.keys(), key=lambda x: (labels[x], x))

    # расписание на машины
    machine_end_times = [0] * m
    machine_schedules = [[] for _ in range(m)]

    task_start = {}
    task_end = {}

    for t in ordered_tasks:
        task_obj = tasks[t]

        # Все предшественники должны быть завершены
        earliest_start = 0
        for pred_task in pred[t]:
            earliest_start = max(earliest_start, task_end[pred_task])

        # Найти первую машину, доступную не ранее earliest_start
        best_machine = None
        best_start = float('inf')
        for i in range(m):
            available_time = max(machine_end_times[i], earliest_start)
            if available_time < best_start:
                best_start = available_time
                best_machine = i
        if best_machine is None:
            print("No solution")
            return []
        
        # Назначить задачу
        task_obj.start_time = best_start
        task_obj.end_time = best_start + task_obj.duration
        task_obj.machine = best_machine

        task_start[t] = task_obj.start_time
        task_end[t] = task_obj.end_time
        machine_end_times[best_machine] = task_obj.end_time
        machine_schedules[best_machine].append(task_obj)

    return machine_schedules

# Пример использования
if __name__ == "__main__":
    # Задачи с одинаковой длительностью 1
    tasks = {i: Task(i) for i in range(1, 10)}
    precedence = {
        1: {3},
        2: {3},
        3: {4},
        4: {5},
        5: {6, 7},
        6: {8},
        7: {8}
    }

    schedule = coffman_graham(tasks, precedence, m=2)
    for i, machine in enumerate(schedule):
        print(f"Машина {i+1}:")
        for task in machine:
            print(f"  Задача {task.id}, начало: {task.start_time}, конец: {task.end_time}")
