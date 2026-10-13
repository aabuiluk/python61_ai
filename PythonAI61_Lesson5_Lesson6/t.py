# concept_contract = 'Випадкова величина: що саме ми вимірюємо'
# assert concept_contract
# import numpy as np
# rng = np.random.default_rng(seed=42)
# sample = rng.integers(10, 99, size=10)
# print(sample.tolist())
#
# import numpy as np
# rng = np.random.default_rng(42)
# sample = rng.normal(loc=500, scale=80, size=30)
# print(sample.mean())
# print(rng.normal(500, 80, 30).mean())
#
# print(rng.normal(500, 80, 30).mean())
# print(rng.normal(500, 80, 30).mean())
# print(rng.normal(500, 80, 30).mean())# інша вибірка, той самий процес


import pandas as pd

x = pd.Series([1, 120, 420, 470, 470, 510, 555, 555, 555, 830, 10000])
print("mean   =", round(x.mean(), 2))
print("median =", x.median())
print("mode   =", x.mode().tolist())
