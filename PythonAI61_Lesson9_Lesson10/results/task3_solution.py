from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def main() -> None:
    X, y = load_diabetes(return_X_y=True)
    x = X[:, 2].reshape(-1, 1)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    y_pred = LinearRegression().fit(x_train, y_train).predict(x_test)

    print("MAE:", round(mean_absolute_error(y_test, y_pred), 3))
    print("MSE:", round(mean_squared_error(y_test, y_pred), 3))
    print("R²:", round(r2_score(y_test, y_pred), 3))


if __name__ == "__main__":
    main()
