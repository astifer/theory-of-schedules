from collections import defaultdict
import heapq

from common import Task, get_graph


def fujii_scheduler(tasks, precedence, m=2):
    """
    Реализация алгоритма Fujii.
    tasks: dict[int, Task]
    precedence: dict[int, set[int]]
    m: количество машин
    """
    time = 0
    in_progress = []
    finished = set()
    ready_queue = []
    machine_end_times = [0] * m
    machine_schedules = [[] for _ in range(m)]

    successors, predecessors = get_graph(precedence)

    for t in tasks.values():
        successors.setdefault(t.id, set())
        predecessors.setdefault(t.id, set())

    # Задачи без предшественников
    available = {t.id for t in tasks.values() if not predecessors.get(t.id, set())}

    while len(finished) < len(tasks):
        # Обновим время
        if in_progress:
            time = min([end for end, _, _ in in_progress])
        else:
            time += 1  # Иначе просто двигаем время вперёд

        # Удалим завершённые
        still_in_progress = []
        for end_time, task_id, machine in in_progress:
            if end_time <= time:
                finished.add(task_id)
                machine_end_times[machine] = end_time
                # Освободить потомков
                for succ in successors[task_id]:
                    if predecessors[succ].issubset(finished):
                        available.add(succ)
            else:
                still_in_progress.append((end_time, task_id, machine))
        in_progress = still_in_progress

        # Готовые задачи
        ready = sorted(
            [t for t in available if t not in finished],
            key=lambda x: tasks[x].duration  # Приоритет — по короткой длительности
        )

        # Распределим задачи по свободным машинам
        free_machines = [i for i in range(m) if all(end > time or mach != i for end, _, mach in in_progress)]

        for i in range(min(len(ready), len(free_machines))):
            t_id = ready[i]
            machine = free_machines[i]
            task = tasks[t_id]
            task.start_time = time
            task.end_time = time + task.duration
            task.machine = machine

            in_progress.append((task.end_time, task.id, machine))
            machine_schedules[machine].append(task)
            available.remove(t_id)

    return machine_schedules


if __name__ == "__main__":
    tasks = {i: Task(i) for i in range(5)}

    precedence = {
        1: {3},
        2: {3},
        3: {4}
    }

    schedule = fujii_scheduler(tasks, precedence, m=2)
    for i, machine in enumerate(schedule):
        print(f"Машина {i+1}:")
        for task in machine:
            print(f"  Задача {task.id}, начало: {task.start_time}, конец: {task.end_time}")
