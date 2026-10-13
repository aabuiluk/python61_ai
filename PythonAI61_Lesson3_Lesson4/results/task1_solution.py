import numpy as np

rng = np.random.default_rng(42)
arr = rng.integers(0, 101, size=101)
print('min:', arr.min(), 'max:', arr.max(), 'mean:', float(arr.mean()))
print('before:', arr)
arr_sorted = np.sort(arr)
print('after:', arr_sorted)

