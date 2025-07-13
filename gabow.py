from common import Task, get_graph
from typing import Dict, List

def gabow_scc(succ: Dict[int, set[int]]) -> List[List[int]]:
    index = 0
    visited = set()
    stack = []
    p_stack = []
    indices = {}
    components = []

    def dfs(v):
        nonlocal index
        indices[v] = index
        index += 1
        stack.append(v)
        p_stack.append(v)
        visited.add(v)

        for w in succ.get(v, []):
            if w not in indices:
                dfs(w)
            elif w not in components_flat:
                while indices[p_stack[-1]] > indices[w]:
                    p_stack.pop()

        if p_stack and p_stack[-1] == v:
            p_stack.pop()
            component = []
            while True:
                u = stack.pop()
                component.append(u)
                components_flat.add(u)
                if u == v:
                    break
            components.append(component)

    components_flat = set()  # все уже обработанные узлы

    for v in succ:
        if v not in indices:
            dfs(v)

    return components


def validate_schedule(precedence):
    succ, pred = get_graph(precedence)
    sccs = gabow_scc(succ)
    for comp in sccs:
        if len(comp) > 1:
            raise ValueError(f"Cycle detected in tasks: {comp}")

if __name__ == '__main__':
    # Граф с циклом: 1 → 2 → 3 → 1
    precedence = {
        1: [3],
        2: [1],
        3: [2],
        4: [],
    }

    succ, pred = get_graph(precedence)
    sccs = gabow_scc(succ)

    print("Сильно связные компоненты:")
    for scc in sccs:
        print(sorted(scc))