"""Пара 21 · ми задаємо розмір і кількість, не числа в ядрі."""

import torch
from torch import nn

layer = nn.Conv2d(3, 16, kernel_size=3)
weight = layer.weight.detach()
print("shape", tuple(weight.shape))
print("one kernel", weight[0].numel())
print("all kernels", weight.numel())
print("sample value", float(weight[0, 0, 0, 0]))
