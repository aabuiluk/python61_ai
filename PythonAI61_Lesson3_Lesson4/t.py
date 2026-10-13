# import numpy as np
#
# numbers = [1, 2, 3, 4]
# print(numbers * 10)
# arr = np.array(numbers, dtype=np.int64)
#
# print(type(numbers), numbers)
# print(type(arr), arr)
# print(arr.dtype, arr.shape, arr.ndim)
# print(arr * 10)
#
# import numpy as np
#
# celsius = np.array([18.0, 21.5, 19.0, 24.5])
# fahrenheit = celsius * 9 / 5 + 32
# mask = celsius >= 20
#
# print("F:", np.round(fahrenheit, 1))
# print("теплі дні:", celsius[mask])
# print("mean:", celsius.mean())
#
# import numpy as np
# a = np.array([[1, 2, 3], [4, 5, 6]])  # (2, 3)
# b = np.array([10, 20, 30])             # (3,) → (1, 3) → (2, 3)
# print(a + b)
# print((a * b).sum(axis=1))

import numpy as np
import pandas as pd

# scores = np.array([92, 88, 95], dtype=np.int64)
# series = pd.Series(scores, index=["Olena", "Taras", "Ira"], name="score")
# df = pd.DataFrame({"name": series.index, "score": series.values, "passed": series.values >= 90})
#
# print(series)
# print(df)

import pandas as pd

df = pd.DataFrame(
    {
        "product": ["SSD", "Mouse", "Keyboard"],
        "price": [2499, 699, 1299],
        "qty": [3, 5, 2],
    }
)
# quantity
df["revenue"] = df["price"] * df["qty"]
df.to_csv("sales_demo.csv", index=False)

loaded = pd.read_csv("sales_demo.csv")
print(loaded.head(2))
print(loaded.columns.tolist())