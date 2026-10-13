"""Пара 15 · завдання 2. Персептрон nn.Linear(1, 1), ручне оновлення."""

import torch
from torch import nn
#
# torch.manual_seed(42)
# x = torch.randn(100, 1)
# y = 0.7 * x + 0.2 + 0.1 * torch.randn_like(x)
# model = nn.Linear(1, 1)
# print("w0", model.weight.item(), "b0", model.bias.item())
# lr = 0.01
# for epoch in range(80):
#     loss = ((model(x) - y) ** 2).mean()
#     loss.backward()
#     with torch.no_grad():
#         model.weight -= lr * model.weight.grad
#         model.bias -= lr * model.bias.grad
#     model.zero_grad()
#     if epoch in (0, 10, 20, 30, 40, 50, 60, 70, 79):
#         print(f"epoch {epoch+1:02d} loss={loss.item():.4f}")
# print("w1", model.weight.item(), "b1", model.bias.item())

import torch
from torch import nn

torch.manual_seed(42)
x = torch.randn(100, 2)
y = 0.7 * x[:, :1] + 0.3 * x[:, 1:] + 0.2 + 0.1 * torch.randn(100, 1)
model = nn.Linear(2, 1)
lr = 0.01
first = last = None
for epoch in range(80):
    pred = model(x)
    loss = ((pred - y) ** 2).mean()
    if epoch == 0:
        first = loss.item()
    loss.backward()
    with torch.no_grad():
        model.weight -= lr * model.weight.grad
        model.bias -= lr * model.bias.grad
    model.zero_grad()
    last = loss.item()
    if epoch in (0, 10, 20, 30, 40, 50, 60, 70, 79):
        print(f"epoch {epoch+1:02d} loss={loss.item():.4f}")
print("Linear(2,1)", round(first, 4), round(last, 4), last < first)
# -> Linear(2,1) first last True