

def greedy_walk(adj, start):
    """
    Simple greedy walk:
    - start from 'start'
    - always go to an unvisited neighbor with smallest degree
    - stop when stuck
    """
    n = len(adj)
    visited = [False] * n
    path = [start]
    visited[start] = True
    current = start

    while True:
        candidates = [v for v in adj[current] if not visited[v]]
        if not candidates:
            break

        # pick neighbor with smallest degree (heuristic)
        next_v = min(candidates, key=lambda v: len(adj[v]))
        visited[next_v] = True
        path.append(next_v)
        current = next_v

    return path


def longest_simple_path_heuristic(adj, num_starts=500, random_seed=None):
    """
    Try 'num_starts' random starting nodes and keep the longest path found.
    """
    n = len(adj)
    if n == 0:
        return []

    if random_seed is not None:
        random.seed(random_seed)

    best_path = []
    nodes_idx = list(range(n))

    for _ in range(num_starts):
        start = random.choice(nodes_idx)
        path = greedy_walk(adj, start)
        if len(path) > len(best_path):
            best_path = path

    return best_path
