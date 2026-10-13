"""Пара 16 · завдання 3. SGD, 20 епох, таблиця loss."""

import torch
from torch import nn

torch.manual_seed(42)
x = torch.randn(100, 1)
y = 0.7 * x + 0.2 + 0.1 * torch.randn_like(x)
model = nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.01)
print("epoch loss")
for epoch in range(20):
    opt.zero_grad()
    loss = nn.functional.mse_loss(model(x), y)
    loss.backward()
    opt.step()
    print(f"{epoch+1:02d} {loss.item():.4f}")
