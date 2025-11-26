from top_k_paths import find_top_k_paths
from graph_util.make_adj_list import process_graphs
from py_extraction.longest_path_extaction import extract_longest_path
import os
import sys
import model.net as net
import pickle

sys.stdout = open("approximate_paths.txt", "w")

base = os.path.dirname(__file__)              
path =  os.path.join(base, "datasets/graphs.txt")
graphs = process_graphs(path, 30)

base = os.path.dirname(__file__)             
pathh = os.path.join(base, "model/trained_model.pkl")
with open(pathh, "rb") as f:
    sys.modules['__main__'] = net
    model = pickle.load(f)

print(len(graphs))
for adj in graphs:
    approx_paths = find_top_k_paths(adj, 4, model)
    best_path = max(approx_paths, key = lambda p: len(p))
    print(len(best_path))
    print(*best_path)

