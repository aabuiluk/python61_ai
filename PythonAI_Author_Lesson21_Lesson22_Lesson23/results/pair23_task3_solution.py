"""Пара 23 · пункт 3. Форма виходу (2, 10)."""

import torch
from torch import nn

model = nn.Sequential(
    nn.Conv2d(1, 16, 3),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(16 * 13 * 13, 10),
)
out = model(torch.zeros(2, 1, 28, 28))
assert tuple(out.shape) == (2, 10)
print(tuple(out.shape))
