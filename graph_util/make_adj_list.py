def process_graphs(input_file, n):
    all_graphs = []
    with open(input_file, 'r') as f:
        t = int(f.readline().strip())

        for i in range(t):
            line = f.readline().strip()
            if line == '':
                line = f.readline().strip()
            m = int(line)
            adj = [[] for _ in range(n)]

            for j in range(m):
                u, v = map(int, f.readline().split())
                adj[u].append(v)

            all_graphs.append(adj)

    return all_graphs
