import numpy as np

rng = np.random.default_rng(42)
arr = rng.integers(0, 101, size=10)
matrix = rng.integers(1, 51, size=(4, 4))

print("before:", arr)
print("after:", np.sort(arr))
print("min/max/mean:", arr.min(), arr.max(), round(arr.mean(), 2))
print()
print("matrix:")
print(matrix)
print("rows:", matrix.sum(axis=1))
print("cols:", matrix.sum(axis=0))
print("mean:", round(matrix.mean(), 2))
