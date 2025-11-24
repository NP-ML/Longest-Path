import make_adj_list
import pipeline3 
from algorithm import feature_extraction
import torch 
import threading
import copy 
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pandas as pd
import pickle 
import time
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(10, 20)  # Input layer to hidden layer, we have 10 features 
        self.fc2 = nn.Linear(20, 20)  # Hidden layer to output layer4
        self.fc3 = nn.Linear(20, 20)  # Hidden layer to output layer
        self.fc4 = nn.Linear(20, 20)  # Hidden layer to output layer
        self.fc5 = nn.Linear(20, 20)  # Hidden layer to output layer
        self.fc6 = nn.Linear(20, 1)  # Hidden layer to output layer

    def forward(self, x):
        ub = x[:, 3:4]
        lb = x[:, 8:9]
        features = x
        y = torch.sigmoid(self.fc1(features))
        y = torch.sigmoid(self.fc2(y))
        y = torch.sigmoid(self.fc3(y))
        y = torch.sigmoid(self.fc4(y))
        y = torch.sigmoid(self.fc5(y))
        y = torch.sigmoid(self.fc6(y))
        return y * (ub - lb) + lb 
path =r"C:\Users\manso\OneDrive\Desktop\E3\fall 2025-2026\EECE 490\EECE 490 project final\Longest-Path\trained_model.pkl"
# trained_model.pkl 

with open(path, "rb") as f:
    model = pickle.load(f)   # <-- NOT torch.load

# bi hay badek graphs_adjlist_sparse 
adj=make_adj_list.process_graph(r"C:\Users\manso\OneDrive\Desktop\E3\fall 2025-2026\EECE 490\EECE 490 project final\Longest-Path\graphs_adjlist_sparse.txt", 30)[3]

# save time here 
#print(pipeline3.top_K_nodes(adj,model,feature_extraction.extract_features,undirected=False,neighbors_only_update=True))
#inference time = time2-time1 
#print inference time 
def run_thread(adj, model, results, idx, param):
    local_adj = copy.deepcopy(adj)
    out = pipeline3.top_K_nodes(
        local_adj,
        model,
        feature_extraction.extract_features,
        undirected=False,
        neighbors_only_update=True,
        k = param
    )
    results[idx] = out
params = [0, 1, 2, 3]  
n = 4
results = [None] * n
t0 = time.perf_counter()
threads = []

for i, p in enumerate(params):
    t = threading.Thread(
        target=run_thread,
        args=(adj, model, results, i, p)   # p is unique for this thread
    )
    threads.append(t)
    t.start()

for t in threads:
    t.join()
t1 = time.perf_counter()

print()
print("Those are the results:")
print()
print(results)
List = []
for i in range (0, len(results)):
    List.append(len(results[i]))
print()
print("\nTotal time:", t1 - t0, "seconds")
print()
print(List)


