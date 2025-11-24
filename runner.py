from top_k_paths import find_top_k_paths
from graph_util.make_adj_list import process_graph
from py_extraction.longest_path_extaction import extract_longest_path
import os
import sys
import model.net as net
import pickle

base = os.path.dirname(__file__)              
path =  os.path.join(base, "datasets/graphs_adjlist_sparse.txt")
adj = process_graph(path, 30)[18]

base = os.path.dirname(__file__)             
pathh = os.path.join(base, "model/trained_model.pkl")
with open(pathh, "rb") as f:
    sys.modules['__main__'] = net
    model = pickle.load(f)

approx_paths = find_top_k_paths(adj, 4, model)
print("Approx_k_longest:")
print(approx_paths)
actual_path= extract_longest_path(adj)
print("Real_longest:")
print(actual_path)
# add accuracy stuf .....
