"""Пара 10 · середнє як baseline vs LinearRegression."""

from sklearn.datasets import load_diabetes
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

X, y = load_diabetes(return_X_y=True)
x_train, x_test, y_train, y_test = train_test_split(X[:, [2]], y, test_size=0.2, random_state=42)

baseline = DummyRegressor(strategy="mean").fit(x_train, y_train)
model = LinearRegression().fit(x_train, y_train)

for name, est in (("mean baseline", baseline), ("LinearRegression", model)):
    pred = est.predict(x_test)
    print(name, "MAE", round(mean_absolute_error(y_test, pred), 3), "R²", round(r2_score(y_test, pred), 3))
