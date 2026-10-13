"""Пара 21 · пункт 2. Linear проти Conv2d."""

from torch import nn

flat = nn.Linear(28 * 28, 10)
conv = nn.Conv2d(1, 16, kernel_size=3)
flat_n = sum(p.numel() for p in flat.parameters())
conv_n = sum(p.numel() for p in conv.parameters())
assert flat_n == 28 * 28 * 10 + 10
assert conv_n == 1 * 16 * 3 * 3 + 16
print("Linear", flat_n)
print("Conv2d", conv_n)
