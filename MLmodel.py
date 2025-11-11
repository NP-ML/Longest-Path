import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pandas as pd
# i have to contryct input
# construct output 
data = pd.read_csv("data.csv").values
x = torch.tensor(data[:, :10], dtype=torch.float32)
y = torch.tensor(data[:, 10:], dtype=torch.float32)
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
        ub = x[:, 0:1]
        lb = x[:, 1:2]
        features = x
        y = torch.sigmoid(self.fc1(features))
        y = torch.sigmoid(self.fc2(y))
        y = torch.sigmoid(self.fc3(y))
        y = torch.sigmoid(self.fc4(y))
        y = torch.sigmoid(self.fc5(y))
        y = torch.sigmoid(self.fc6(y))
        return y * (ub - lb) + lb # it is gonna return a prediction of the longest path starting from a certain node 

net = Net()
criterion = nn.MSELoss()
optimizer = optim.Adam(net.parameters(), lr=0.01)
epochs = 5000
loss_list = []
for epoch in range(epochs):
    optimizer.zero_grad()        # clear old gradients
    output = net(x)              # forward
    loss = criterion(output, y)  # compute loss
    loss.backward()              # backprop
    optimizer.step()             # update weights

    if epoch % 100 == 0:
        l = loss.item()
        print(f'Epoch [{epoch}/{epochs}], Loss: {l:.6f}')
        loss_list.append(l)