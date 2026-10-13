from sklearn.datasets import make_regression
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


def main() -> None:
    X, y = make_regression(n_samples=500, n_features=20, n_informative=5, noise=10, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "LinearRegression": LinearRegression(),
        "Lasso": Lasso(alpha=0.1),
        "Ridge": Ridge(alpha=1.0),
    }
    for name, model in models.items():
        model.fit(X_train, y_train)
        nz = int((model.coef_ != 0).sum())
        print(name, "R²", round(r2_score(y_test, model.predict(X_test)), 3), "nonzero", nz)


if __name__ == "__main__":
    main()
