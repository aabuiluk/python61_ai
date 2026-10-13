"""Пара 19 · складніше: clip_grad_norm_ на випадкових градієнтах."""

import torch
from torch import nn
m = nn.Linear(4, 4)
x = torch.randn(8, 4)
loss = m(x).pow(2).mean()
loss.backward()
print(torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0))
