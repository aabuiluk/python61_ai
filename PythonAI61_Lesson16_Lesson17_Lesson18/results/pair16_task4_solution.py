"""Пара 16 · завдання 4. Графік MSE vs epoch."""

from pathlib import Path

import matplotlib.pyplot as plt
import torch
from torch import nn

torch.manual_seed(42)
x = torch.randn(100, 1)
y = 0.7 * x + 0.2 + 0.1 * torch.randn_like(x)
model = nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.01)
hist = []
for _ in range(20):
    opt.zero_grad()
    loss = nn.functional.mse_loss(model(x), y)
    loss.backward()
    opt.step()
    hist.append(loss.item())

plt.plot(range(1, 21), hist, marker="o")
plt.xlabel("epoch")
plt.ylabel("MSE")
plt.title("HealthRisk · loss")
out = Path(__file__).with_name("loss_healthrisk.png")
plt.savefig(out, dpi=120, bbox_inches="tight")
print("saved", out)
