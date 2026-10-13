import numpy as np

rng = np.random.default_rng(42)
m = rng.random((10, 10))
print('min:', m.min(), 'at', np.unravel_index(m.argmin(), m.shape))
print('max:', m.max(), 'at', np.unravel_index(m.argmax(), m.shape))
