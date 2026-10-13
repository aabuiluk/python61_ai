from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures


def main() -> None:
    X, y = make_regression(n_samples=200, n_features=1, noise=15, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    for degree in (1, 2, 5, 10):
        model = Pipeline([
            ("poly", PolynomialFeatures(degree=degree)),
            ("reg", LinearRegression()),
        ]).fit(X_train, y_train)
        print(
            f"degree={degree}",
            "train", round(r2_score(y_train, model.predict(X_train)), 3),
            "test", round(r2_score(y_test, model.predict(X_test)), 3),
        )


if __name__ == "__main__":
    main()
