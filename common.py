from collections import defaultdict, deque

class Task:
    def __init__(self, id, duration: int = 1):
        self.id = id
        self.duration = duration
        self.start_time = None
        self.end_time = None
        self.machine = None

def get_graph(precedence):
    #обратный графs
    succ = defaultdict(set)
    pred = defaultdict(set)
    for u in precedence:
        for v in precedence[u]:
            succ[u].add(v)
            pred[v].add(u)

    return succ, pred