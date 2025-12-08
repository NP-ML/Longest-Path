# generalisation/dataset_generalisation_compare.py
#
# Run the trained model and a simple greedy heuristic on all graphs
# in datasets/graphs.txt and compare path lengths.
#
# Outputs per-graph details + global averages.

from top_k_paths import find_top_k_paths
from graph_util.make_adj_list import process_graphs
import model.net as net
from bench_mark import heuristic
import os
import sys
import pickle
import random

TOP_K = 4                 # k for find_top_k_paths
NUM_STARTS_GREEDY = 1000  # random restarts for greedy
RESULTS_FILE = "approximate_paths_compare.txt"
MODEL_FILE = "trained_model2.pkl"


# ==============================
# Helper: detect max node label
# ==============================

def detect_max_node_label(graphs_path):
    """
    Scan the raw graphs.txt file and return the largest integer token seen.
    Assumes node labels are integers.
    """
    max_label = -1
    with open(graphs_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            for tok in line.split():
                try:
                    v = int(tok)
                except ValueError:
                    continue
                if v > max_label:
                    max_label = v
    return max_label


# ==============================
# 1) Load graphs
# ==============================

def load_graphs():
    base = os.path.dirname(__file__)
    graphs_path = os.path.join(base, "datasets", "graphs.txt")

    max_nodes = detect_max_node_label(graphs_path)
    print(f"Detected max node label in dataset: {max_nodes}")

    # use that as the max_nodes parameter
    graphs = process_graphs(graphs_path, max_nodes)
    return graphs


# ==============================
# 2) Load trained model
# ==============================

def load_model():
    base = os.path.dirname(__file__)
    model_path = os.path.join(base, "model", MODEL_FILE)
    with open(model_path, "rb") as f:
        # so pickle can resolve classes defined in model.net
        sys.modules["__main__"] = net
        model = pickle.load(f)
    print("Loaded model from:", model_path)
    return model




# ==============================
# 3) Pipeline wrappers
# ==============================

def run_model_pipeline(adj, model, k=TOP_K):
    """
    Your learned heuristic: returns best path among top-k.
    """
    approx_paths = find_top_k_paths(adj, k, model)
    if not approx_paths:
        return []
    return max(approx_paths, key=len)


def run_greedy_pipeline(adj, num_starts=NUM_STARTS_GREEDY, seed=None):
    """
    Greedy heuristic: returns longest path found by random restarts.
    """
    return longest_simple_path_heuristic(adj, num_starts=num_starts, random_seed=seed)


# ==============================
# 5) Main comparison + averages
# ==============================

def main():
    graphs = load_graphs()
    model = load_model()

    model_lengths = []
    greedy_lengths = []

    with open(RESULTS_FILE, "w", encoding="utf-8") as out:
        out.write(f"Number of graphs: {len(graphs)}\n")
        out.write(f"Model file: {MODEL_FILE}\n\n")

        for g_idx, adj in enumerate(graphs):
            n = len(adj)

            # --- your model-based pipeline ---
            model_path = run_model_pipeline(adj, model)
            L_model = len(model_path)

            # --- greedy heuristic pipeline ---
            greedy_path = heuristic.run_greedy_pipeline(adj, seed=g_idx)
            L_greedy = len(greedy_path)

            model_lengths.append(L_model)
            greedy_lengths.append(L_greedy)

            out.write(f"Graph {g_idx}:\n")
            out.write(f"  #nodes             : {n}\n")
            out.write(f"  model path length  : {L_model}\n")
            out.write(f"  greedy path length : {L_greedy}\n")
            out.write(f"  model path nodes   : {model_path}\n")
            out.write(f"  greedy path nodes  : {greedy_path}\n\n")

        # ===== Averages =====
        n_graphs = len(model_lengths)
        if n_graphs > 0:
            avg_model = sum(model_lengths) / n_graphs
            avg_greedy = sum(greedy_lengths) / n_graphs
            improvements = [m - g for m, g in zip(model_lengths, greedy_lengths)]
            avg_improvement = sum(improvements) / n_graphs

            out.write("=== Summary ===\n")
            out.write(f"#graphs                : {n_graphs}\n")
            out.write(f"avg model length       : {avg_model:.3f}\n")
            out.write(f"avg greedy length      : {avg_greedy:.3f}\n")
            out.write(f"avg improvement (diff) : {avg_improvement:.3f}\n")

            print("=== Summary ===")
            print(f"#graphs                : {n_graphs}")
            print(f"avg model length       : {avg_model:.3f}")
            print(f"avg greedy length      : {avg_greedy:.3f}")
            print(f"avg improvement (diff) : {avg_improvement:.3f}")
        else:
            out.write("No graphs found.\n")
            print("No graphs found.")


if __name__ == "__main__":
    main()
