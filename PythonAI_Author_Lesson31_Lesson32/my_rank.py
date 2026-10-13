import numpy as np
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler

X_scaled = StandardScaler().fit_transform(load_wine().data)
s = np.linalg.svd(X_scaled, compute_uv=False)        # 13 сингулярних чисел
share = (s ** 2).cumsum() / (s ** 2).sum()            # накопичена частка: share[0] — це k = 1
print(share[1].round(3))                              # k = 2 → 0.554
# Міні-завдання 5: надрукуйте частку і похибку відновлення √(1 − частка) для k = 4
