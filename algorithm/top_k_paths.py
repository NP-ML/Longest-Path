import copy
import threading
from algorithm import path_from_kth_best_start

def find_top_k_paths(adj, k, model):

    def run_thread(adj, model, results, idx, param):
        local_adj = copy.deepcopy(adj)
        results[idx] = path_from_kth_best_start(
            local_adj,
            model,
            k=param
        )

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
