from common import Task, get_graph

def sethi_ulman_schedule(succ: dict[int, set[int]], pred: dict[int, set[int]]) -> list[int]:
    # Кэш для подсчёта register need
    reg_need_cache = {}

    def register_need(node: int) -> int:
        if node in reg_need_cache:
            return reg_need_cache[node]
        if not succ.get(node):  # лист — нет потомков
            reg_need_cache[node] = 1
        else:
            reg_need_cache[node] = max(register_need(child) for child in succ[node]) + 1
        return reg_need_cache[node]

    remaining = set(succ.keys()) | set(pred.keys())
    schedule = []

    while remaining:
        # Найти листья (у которых либо нет succ, либо все succ уже в расписании)
        leaves = [
            task for task in remaining
            if not succ.get(task) or succ[task].issubset(schedule)
        ]
        if not leaves:
            raise ValueError("Граф содержит цикл!")

        # Выбрать leaf с минимальным register_need
        leaves.sort(key=register_need)
        chosen = leaves[0]

        schedule.insert(0, chosen)  # добавляем в начало — инверсное построение
        remaining.remove(chosen)

    return schedule

if __name__ == '__main__':
    tasks = {
        1: Task(1),
        2: Task(2),
        3: Task(3),
        4: Task(4)
    }


    precedence = {
        1: {},
        2: {},
        3: {1, 2},
        4: {3},
    }
    succ, pred = get_graph(precedence)

    schedule = sethi_ulman_schedule(succ, pred)
    print("Sethi–Ulman порядок выполнения:", schedule)
