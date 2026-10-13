import numpy as np

rng = np.random.default_rng(42)
arr = rng.integers(-10, 11, size=15)
print('arr:', arr)
print('positive:', arr[arr > 0])
print('even:', arr[arr % 2 == 0])
