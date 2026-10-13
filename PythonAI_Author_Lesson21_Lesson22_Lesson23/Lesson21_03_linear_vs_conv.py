"""Пара 21 · скільки ваг у рядка пікселів і в маленького ядра."""

import torch
from torch import nn

flat = nn.Linear(28 * 28, 10)
conv = nn.Conv2d(1, 16, kernel_size=3)
print("Linear", sum(p.numel() for p in flat.parameters()))
print("Conv2d", sum(p.numel() for p in conv.parameters()))
