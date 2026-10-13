"""Пара 13 · gap train/test як сигнал overfitting."""

from sklearn.datasets import fetch_california_housing
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

df = fetch_california_housing(as_frame=True).frame
X = df.drop(columns=["MedHouseVal"])
y = df["MedHouseVal"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"{'depth':>8} {'train':>8} {'test':>8} {'gap':>8}")
for depth in (2, 4, 8, 16, None):
    tree = DecisionTreeRegressor(max_depth=depth, random_state=42).fit(X_train, y_train)
    tr = r2_score(y_train, tree.predict(X_train))
    te = r2_score(y_test, tree.predict(X_test))
    print(f"{str(depth):>8} {tr:8.3f} {te:8.3f} {tr - te:8.3f}")
