import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(10, 20)
        self.fc2 = nn.Linear(20, 20)
        self.fc3 = nn.Linear(20, 20)
        self.fc4 = nn.Linear(20, 20)
        self.fc5 = nn.Linear(20, 20)
        self.fc6 = nn.Linear(20, 1)

    def forward(self, x):
        ub = x[:, 3:4]
        lb = x[:, 8:9]
        y = torch.sigmoid(self.fc1(x))
        y = torch.sigmoid(self.fc2(y))
        y = torch.sigmoid(self.fc3(y))
        y = torch.sigmoid(self.fc4(y))
        y = torch.sigmoid(self.fc5(y))
        y = torch.sigmoid(self.fc6(y))
        return y * (ub - lb) + lb
