# generalisation/les_miserables_generalisation.py
#
# Run the trained model on the Les Misérables character network
# and print the top-k paths (indices + lengths).

from top_k_paths import find_top_k_paths
import model.net as net
import networkx as nx
import os
import sys
import pickle

TOP_K = 4
MODEL_FILE = "trained_model2.pkl"


def build_lesmis_adj():
    """
    Load the Les Misérables co-appearance graph from NetworkX
    and convert it to a 0-based adjacency list (list of lists).
    Returns (nodes, adj), where:
      - nodes[i] = character name of node i
      - adj[i]   = list of neighbor indices of node i
    """
    G = nx.les_miserables_graph()

    print("Les Mis graph:")
    print("  Nodes:", G.number_of_nodes())
    print("  Edges:", G.number_of_edges())

    nodes = list(G.nodes())
    node_to_idx = {n: i for i, n in enumerate(nodes)}

    adj = [[] for _ in range(len(nodes))]
    for u, v in G.edges():
        i = node_to_idx[u]
        j = node_to_idx[v]
        adj[i].append(j)
        adj[j].append(i)  # undirected

    return nodes, adj


def load_model():
    """
    Load the trained model from model/MODEL_FILE using pickle.
    """
    base = os.path.dirname(__file__)
    model_path = os.path.join(base, "model", MODEL_FILE)

    with open(model_path, "rb") as f:
        # so pickle can resolve classes defined in model.net
        sys.modules["__main__"] = net
        model = pickle.load(f)

    print("Loaded model from:", model_path)
    return model


def main():
    nodes, adj = build_lesmis_adj()
    model = load_model()

    # Treat Les Mis as a single graph
    approx_paths = find_top_k_paths(adj, TOP_K, model)

    print("\nTop-k approximate paths (indices):")
    for k, path in enumerate(approx_paths):
        print(f"  Path {k}: length={len(path)}, nodes={path}")

    # Optionally: show the best path with character names
    if approx_paths:
        best_path = max(approx_paths, key=len)
        char_path = [nodes[i] for i in best_path]

        print("\nBest path:")
        print("  Length:", len(best_path))
        print("  Indices:", best_path)
        print("  Characters:")
        print("   ", " -> ".join(char_path))


if __name__ == "__main__":
    main()
