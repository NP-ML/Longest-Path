import make_adj_list
import pipeline3 
from algorithm import feature_extraction
import torch 
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pandas as pd
import pickle 
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
path = r"C:\Users\User\Longest-Path-2\trained_model.pkl"

with open(path, "rb") as f:
    model = pickle.load(f)   # <-- NOT torch.load



adj=make_adj_list.process_graph(r"C:\Users\User\Longest-Path-2\graphs_adjlist_sparse.txt", 30)[3]
print(adj)
print(pipeline3.top_K_nodes(adj,model,feature_extraction.extract_features,undirected=False,neighbors_only_update=True))

