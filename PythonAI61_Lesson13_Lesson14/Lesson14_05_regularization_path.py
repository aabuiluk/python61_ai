"""Пара 14 · Ridge: як alpha стискає коефіцієнти."""

from sklearn.datasets import make_regression
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split

X, y = make_regression(n_samples=400, n_features=12, n_informative=4, noise=12, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

print(f"{'alpha':>8} {'R²':>8} {'l2_norm':>10}")
for alpha in (0.01, 0.1, 1.0, 10.0, 100.0):
    model = Ridge(alpha=alpha).fit(X_train, y_train)
    r2 = model.score(X_test, y_test)
    nrm = float((model.coef_ ** 2).sum() ** 0.5)
    print(f"{alpha:8} {r2:8.3f} {nrm:10.3f}")
