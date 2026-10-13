"""Пара 21 · пункт 4. 27 чисел в одному ядрі, 432 у шарі."""

from torch import nn

layer = nn.Conv2d(3, 16, kernel_size=3)
weight = layer.weight.detach()
assert tuple(weight.shape) == (16, 3, 3, 3)
assert weight[0].numel() == 27
assert weight.numel() == 432
print(tuple(weight.shape), weight[0].numel(), weight.numel())
