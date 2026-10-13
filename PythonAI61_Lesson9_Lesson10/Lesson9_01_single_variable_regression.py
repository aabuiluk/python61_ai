from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def main() -> None:
    X, y = load_diabetes(return_X_y=True)
    x = X[:, 2].reshape(-1, 1)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model = LinearRegression().fit(x_train, y_train)
    y_pred = model.predict(x_test)

    print("coef:", round(float(model.coef_[0]), 4), "intercept:", round(float(model.intercept_), 4))
    for real, pred in zip(y_test[:10], y_pred[:10]):
        print(f"{real:8.2f}  →  {pred:8.2f}")


if __name__ == "__main__":
    main()
