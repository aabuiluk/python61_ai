"""Пара 23 · один прохід: 2 кадри цифр → 10 сирих рахунків."""

import torch
from torch import nn

model = nn.Sequential(
    nn.Conv2d(1, 16, 3),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(16 * 13 * 13, 10),
)
batch = torch.zeros(2, 1, 28, 28)
print(tuple(model(batch).shape))
