# from sklearn.datasets import fetch_california_housing
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import cross_val_score
# from sklearn.pipeline import make_pipeline
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import r2_score
#
#
# X, y = fetch_california_housing(return_X_y=True)
# X1, y1 = fetch_california_housing(return_X_y=True)
#
# pipe = make_pipeline(StandardScaler(), LinearRegression())
# pipe1 = make_pipeline(StandardScaler(), LinearRegression())
# scores = cross_val_score(pipe, X, y, cv=5, scoring="r2")
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# model = LinearRegression().fit(X_train, y_train)
# print("R²:", round(r2_score(y_test, model.predict(X_test)), 3))
# print("5 оцінок:", scores.round(3).tolist())
# print(f"середнє {scores.mean():.3f} ± {scores.std():.3f}")
# l = scores.round(3).tolist()
#
#
#
#
#
# # -> оцінки помітно різняться між фолдами; середнє ≈ 0.55
# # --- графік ---
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots(figsize=(6, 3.2))
# ax.bar(range(1, len(scores) + 1), scores, color="#5b8def")
# ax.axhline(scores.mean(), color="crimson", linestyle="--",
#            label=f"середнє {scores.mean():.3f}")
# ax.set_xlabel("фолд"); ax.set_ylabel("R²"); ax.set_title("Пʼять оцінок CV")
# ax.legend(); plt.tight_layout(); plt.show()


import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

rng = np.random.default_rng(42)
x = np.linspace(-3, 3, 200)
y = 0.8 * x ** 2 + rng.normal(0, 1.2, x.size)   # парабола + шум

Xtr, Xte, ytr, yte = train_test_split(x.reshape(-1, 1), y, test_size=0.3, random_state=42)
line = LinearRegression().fit(Xtr, ytr)
curve = make_pipeline(PolynomialFeatures(15), LinearRegression()).fit(Xtr, ytr)

print("пряма  R2 test:", round(r2_score(yte, line.predict(Xte)), 2))
print("degree=2 R2 test:", round(r2_score(yte, curve.predict(Xte)), 2))

# -> пряма ≈ 0 (симетрична парабола — пряма безпорадна); degree=2 ≈ 0.77
# --- графік ---
import matplotlib.pyplot as plt
grid = np.linspace(-3, 3, 300).reshape(-1, 1)
fig, ax = plt.subplots(figsize=(6.5, 3.5))
ax.scatter(Xtr, ytr, s=12, alpha=0.45, label="train")
ax.plot(grid, line.predict(grid), color="gray", label="пряма")
ax.plot(grid, curve.predict(grid), color="crimson", label="degree=2")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend(); ax.set_title("Пряма vs крива")
plt.tight_layout(); plt.show()
