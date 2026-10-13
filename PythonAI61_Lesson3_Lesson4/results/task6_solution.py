import numpy as np

a = np.arange(1, 6)
b = np.arange(6, 11)
print('concatenated:', np.concatenate([a, b]))
print('row stack:\n', np.row_stack([a, b]))
print('column stack:\n', np.column_stack([a, b]))
