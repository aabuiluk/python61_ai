"""Пара 15 · середнє: один nn.Linear на синтетичному BMI."""

import torch
from torch import nn

torch.manual_seed(0)
x = torch.randn(64, 1)
y = 0.4 * x + 0.1 + 0.05 * torch.randn_like(x)
model = nn.Linear(1, 1)
print("start", model.weight.item(), model.bias.item())
pred = model(x)
print("mse", ((pred - y) ** 2).mean().item())
# -> start: випадкові w і b (seed 0 фіксує їх)
# -> mse: додатне число, шар ще не навчений
