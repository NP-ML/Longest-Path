import random

def greedy_walk(adj, start):
    """
    adj: list-of-lists adjacency list (0..n-1)
    start: starting node index
    returns: a path (list of node indices), simple (no repeats)
    """
    n = len(adj)
    visited = [False] * n
    path = [start]
    visited[start] = True
    current = start

    while True:
        # unvisited neighbors
        candidates = [v for v in adj[current] if not visited[v]]
        if not candidates:
            break

        # heuristic: pick neighbor with smallest degree
        next_v = min(candidates, key=lambda v: len(adj[v]))

        visited[next_v] = True
        path.append(next_v)
        current = next_v

    return path


def longest_simple_path_heuristic(adj, num_starts=200, random_seed=None):
    """
    Heuristic longest simple path in an undirected graph.

    adj: list-of-lists adjacency list
    num_starts: how many random starting nodes to try
    random_seed: set for reproducibility

    returns: best_path (list of node indices)
    """
    n = len(adj)
    if n == 0:
        return []

    if random_seed is not None:
        random.seed(random_seed)

    best_path = []
    nodes = list(range(n))

    for _ in range(num_starts):
        start = random.choice(nodes)
        path = greedy_walk(adj, start)
        if len(path) > len(best_path):
            best_path = path

    return best_path
