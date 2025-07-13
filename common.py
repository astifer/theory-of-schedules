from collections import defaultdict, deque
from typing import Dict, Set, Tuple

class Task:
    def __init__(self, id, duration: int = 1):
        self.id = id
        self.duration = duration
        self.start_time = None
        self.end_time = None
        self.machine = None


def get_graph(precedence: Dict[int, Set[int]]) -> Tuple[Dict[int, Set[int]], Dict[int, Set[int]]]:
    """
    Построить два словаря:
      successors[u] = множество v, таких что u → v
      predecessors[v] = множество u, таких что u → v
    Работает даже если в precedence встречаются вершины только в значениях.
    """
    # Собираем все вершины: и ключи, и те, что в значениях
    all_nodes = set(precedence.keys())
    for vs in precedence.values():
        all_nodes |= set(vs)

    # Инициализируем
    successors = {node: set() for node in all_nodes}
    predecessors = {node: set() for node in all_nodes}

    # Заполняем рёбрами
    for u, vs in precedence.items():
        for v in vs:
            successors[u].add(v)
            predecessors[v].add(u)

    return successors, predecessors