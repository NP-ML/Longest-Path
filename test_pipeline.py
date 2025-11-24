import pickle
import pipeline3
from algorithm import feature_extraction
import copy
import threading
import sys
import net
import os

def find_k_path(adj, k):
    base = os.path.dirname(__file__)              # folder where test_pipeline.py is
    pathh = os.path.join(base, "trained_model.pkl")
    with open(pathh, "rb") as f:
        sys.modules['__main__'] = net
        model = pickle.load(f)

    def run_thread(adj, model, results, idx, param):
        local_adj = copy.deepcopy(adj)
        out = pipeline3.top_K_nodes(
            local_adj,
            model,
            feature_extraction.extract_features,
            undirected=False,
            neighbors_only_update=True,
            k=param
        )
        results[idx] = out

    params = list(range(k))
    results = [None] * k

    threads = []
    for i, p in enumerate(params):
        t = threading.Thread(target=run_thread, args=(adj, model, results, i, p))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return results
