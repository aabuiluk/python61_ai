"""Пара 3 · складніше. Булева маска, зріз, статистика матриці."""

import numpy as np

rng = np.random.default_rng(7)
scores = rng.integers(40, 101, size=15)
print("scores:", scores)
print("passed (>=60):", scores[scores >= 60])
print("share passed:", round(float((scores >= 60).mean()), 2))

matrix = rng.integers(1, 21, size=(5, 4))
print("\nmatrix:\n", matrix)
print("max per row:", matrix.max(axis=1))
print("arg max col of row 0:", int(matrix[0].argmax()))
print("center 3x2:\n", matrix[1:4, 1:3])
print("where > 15:\n", np.argwhere(matrix > 15))
print("OK")
