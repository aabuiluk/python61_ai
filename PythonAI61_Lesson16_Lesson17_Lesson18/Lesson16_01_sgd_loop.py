"""Пара 16 · легко: SGD loop на 5 епохах."""

import torch
from torch import nn

torch.manual_seed(0)
x = torch.randn(32, 1)
y = 0.5 * x
model = nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.05)
for epoch in range(5):
    opt.zero_grad()
    loss = ((model(x) - y) ** 2).mean()
    loss.backward()
    opt.step()
    print(epoch, loss.item())
# -> 5 рядків: epoch і loss; loss на епосі 4 менший, ніж на 0
