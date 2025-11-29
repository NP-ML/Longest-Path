import random
from algorithm import feature_extraction 
import csv
import plot_graph

def generate_simple_path_graph(N):
    adj = [[] for _ in range(N)]
    for i in range(N - 1): adj[i].append(i + 1)
    return adj

def generate_scc_clique(M):
    adj = [[] for _ in range(M)]
    for u in range(M):
        for v in range(M):
            if u != v: adj[u].append(v)
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
        scc = generate_scc_clique(M)
        for nbrs in scc:
            adj.append([v + off for v in nbrs])  # shift SCC nodes
        entry = off + random.randrange(M)
        adj[hook].append(entry)                  # hook -> SCC
        off += M
    return adj

def generate_chain_with_scc(N, k):
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

    # make them a directed clique + edges to j+1
    for u in scc_nodes:
        for v in scc_nodes:
            if u != v: adj[u].append(v)
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
            L[i] = chain_len + k-1   # can use SCC, gets +k bonus
        else:
            L[i] = chain_len       # after SCC, just chain tail

    # SCC extra nodes N..N+k-1 all have same value as node j
    base = (N - 1 - j) + k-1
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

            # extract features
            # feats = feature_extraction.extract_features(adj)

            # # compute labels (longest simple path lengths)
            # labels = longest_path_labels_chain_scc(N_chain, j, k)

            # # append labels + write to csv
            # total_nodes = len(adj)
            # for i in range(total_nodes):
            #     feats[i].append(labels[i])
            #     writer.writerow(feats[i])

    print("Dataset generation complete.")
