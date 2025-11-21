def process_graph(input_file, N,i=0):
    #i is index in the txt file
    with open(input_file, 'r') as in_file:
        all_graphs = []
        t = int(in_file.readline().strip())

        for _ in range(t):
            m= in_file.readline().strip()
            if m == '' :
                all_graphs.append(adj)
                m= in_file.readline().strip()
                # process one example for now, should fix later
            m = int(m)
            adj = [[] for _ in range(N)]  # Pre-allocated list of lists
            
            for _ in range(m):
                u, v = map(int, in_file.readline().split())
                adj[u].append(v)        
    return all_graphs
