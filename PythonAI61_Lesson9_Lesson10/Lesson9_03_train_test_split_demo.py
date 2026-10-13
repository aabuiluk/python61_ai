"""Пара 9 · навіщо split: навчити на train, перевірити на test."""

from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

X, y = load_diabetes(return_X_y=True)
x = X[:, [2]]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
model = LinearRegression().fit(x_train, y_train)

print("n train:", len(y_train), "n test:", len(y_test))
print("R² train:", round(r2_score(y_train, model.predict(x_train)), 3))
print("R² test :", round(r2_score(y_test, model.predict(x_test)), 3))
print("coef:", round(float(model.coef_[0]), 3), "intercept:", round(float(model.intercept_), 3))
