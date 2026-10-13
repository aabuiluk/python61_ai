"""Пара 16 · складніше: training loop і графік MSE."""

from pathlib import Path

import matplotlib.pyplot as plt
import torch
from torch import nn

torch.manual_seed(0)
x = torch.randn(32, 1)
y = 0.5 * x + 0.1 * torch.randn_like(x)
model = nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.1)
hist = []
for _ in range(8):
    opt.zero_grad()
    loss = ((model(x) - y) ** 2).mean()
    loss.backward()
    opt.step()
    hist.append(loss.item())

out = Path(__file__).with_suffix(".png")
plt.plot(range(1, len(hist) + 1), hist, marker="o")
plt.xlabel("epoch")
plt.ylabel("MSE")
plt.savefig(out, dpi=120, bbox_inches="tight")
print("start", round(hist[0], 4), "end", round(hist[-1], 4))
print("saved", out)
# -> end < start; поруч зі скриптом з’явиться Lesson16_03_loss_plot.png
