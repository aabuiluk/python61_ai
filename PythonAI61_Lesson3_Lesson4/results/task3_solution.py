import numpy as np

arr = np.arange(15)
arr = arr.reshape((3, 5))
print('original:', arr)
print('transposed:', arr.T)
print('reshaped 5x3:', arr.reshape(5, 3))
