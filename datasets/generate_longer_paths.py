import random
from algorithm import feature_extraction 
import csv
import plot_graph

def generate_simple_path_graph(N):
    adj = [[] for _ in range(N)]
    for i in range(N - 1):
        adj[i].append(i + 1)
    return adj

def generate_scc(M, extra_edge_prob=0.3):
    """
    Generate a random strongly connected component on M nodes.

    Construction:
    1) Start with a directed cycle: 0 -> 1 -> ... -> M-1 -> 0
       (guarantees strong connectivity + Hamiltonian cycle).
    2) Add random extra directed edges between distinct nodes
       with probability extra_edge_prob.
    """
    adj = [[] for _ in range(M)]

    # base cycle
    for u in range(M):
        v = (u + 1) % M
        adj[u].append(v)

    # sprinkle random extra edges
    for u in range(M):
        for v in range(M):
            if u == v:
                continue
            if random.random() < extra_edge_prob and v not in adj[u]:
                adj[u].append(v)

    return adj

def generate_graph_with_sccs(N, M_min, M_max, max_sccs):
    adj = generate_simple_path_graph(N)
    num_sccs = random.randint(1, max_sccs)
    hooks = random.sample(range(N - 1), k=min(num_sccs, N - 1))  # don’t hook at last node
    off = N
    for hook in hooks:
        max_allowed = min(M_max, N - 1 - hook)   # ensure M ≤ N-1-hook
        if max_allowed < M_min: 
            continue
        M = random.randint(M_min, max_allowed)

        # random SCC instead of clique
        scc = generate_scc(M)

        # append SCC nodes, shifted
        for nbrs in scc:
            adj.append([v + off for v in nbrs])

        # hook into a random node of this SCC
        entry = off + random.randrange(M)
        adj[hook].append(entry)                  # hook -> SCC
        off += M
    return adj

def generate_chain_with_scc(N, k, extra_edge_prob=0.3):
    # nodes: 0..N-1 are the chain, N..N+k-1 are extra SCC nodes
    total = N + k
    adj = [[] for _ in range(total)]

    # base chain 0 -> 1 -> ... -> N-1
    for i in range(N - 1):
        adj[i].append(i + 1)

    # pick j so that j+1 exists
    j = random.randint(0, N - 2)

    # SCC nodes: j plus the k new ones
    scc_nodes = [j] + list(range(N, N + k))

    # ---- base cycle over scc_nodes (keeps SCC + Hamiltonian path) ----
    # j -> N -> N+1 -> ... -> N+k-1 -> j
    for idx, u in enumerate(scc_nodes):
        v = scc_nodes[(idx + 1) % len(scc_nodes)]
        adj[u].append(v)

    # ---- add random extra edges among SCC nodes ----
    for u in scc_nodes:
        for v in scc_nodes:
            if u == v:
                continue
            if random.random() < extra_edge_prob and v not in adj[u]:
                adj[u].append(v)

    # edges from SCC to j+1 (as in your original code)
    for u in scc_nodes:
        adj[u].append(j + 1)

    return adj, j, k, N  # N is the chain length

def longest_path_labels_chain_scc(N, j, k):
    # returns list L over total_nodes = N + k
    total = N + k
    L = [0] * total

    # chain nodes 0..N-1
    for i in range(N):
        chain_len = N - 1 - i
        if i <= j:
            # can exploit SCC once → extra (k - 1) “bonus” as per your design
            L[i] = chain_len + k - 1
        else:
            L[i] = chain_len

    # SCC extra nodes N..N+k-1 all have same value as node j
    base = (N - 1 - j) + k - 1
    for u in range(N, total):
        L[u] = base

    return L

if __name__ == "__main__":
    random.seed(42)

    N_min, N_max = 41, 200

    # open CSV once
    with open("dataset2.csv", "w", newline="") as f:
        writer = csv.writer(f)

        # header
        header = [f"f{i}" for i in range(1, 11)] + ["target"]
        writer.writerow(header)

        for _ in range(10000):
            # sample chain length
            N = random.randint(N_min, N_max)

            # choose SCC size k however you like
            k = random.randint(10, N - 30)   # ensure room after j

            # generate graph
            adj, j, k, N_chain = generate_chain_with_scc(N, k)

            extract features + labels (still commented like your original)
            feats = feature_extraction.extract_features(adj)
            labels = longest_path_labels_chain_scc(N_chain, j, k)
            total_nodes = len(adj)
            for i in range(total_nodes):
                feats[i].append(labels[i])
                writer.writerow(feats[i])

    print("Dataset generation complete.")
