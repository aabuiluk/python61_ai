import numpy as np

rng = np.random.default_rng(42)
m = rng.integers(1, 51, size=(4, 4))
print(m)
print('rows:', m.sum(axis=1))
print('cols:', m.sum(axis=0))
print('mean:', round(float(m.mean()), 2))
