"""Пара 3 · середній рівень. reshape, вісь, broadcasting."""

import numpy as np

rng = np.random.default_rng(0)
a = rng.integers(1, 10, size=12)
print("flat:", a)
print("3x4:\n", a.reshape(3, 4))
print("2x3x2 shape:", a.reshape(2, 3, 2).shape)

m = np.arange(1, 7).reshape(2, 3)
print("\nmatrix:\n", m)
print("row means:", m.mean(axis=1))
print("col sums:", m.sum(axis=0))

# broadcasting: додати вектор до кожного рядка
shift = np.array([10, 20, 30])
print("\nm + shift:\n", m + shift)
print("OK")
