"""Пара 19 · середнє: три голови під три задачі."""

from torch import nn
print("bin", nn.Linear(16, 1))
print("cls", nn.Linear(16, 3))
print("reg", nn.Linear(16, 1))
