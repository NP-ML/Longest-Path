from test_pipeline import find_k_path
from make_adj_list import process_graph
from algorithm.brute_force import extract_longest_path

import os
base = os.path.dirname(__file__)              
path =  os.path.join(base, "graphs_adjlist_sparse.txt")
adj = process_graph(path, 30)[18]
approx_paths=find_k_path(adj, 4)
print("Approx_k_longest:")
print(approx_paths)
actual_path= extract_longest_path(adj)
print("Real_longest:")
print(actual_path)
# add accuracy stuf .....
