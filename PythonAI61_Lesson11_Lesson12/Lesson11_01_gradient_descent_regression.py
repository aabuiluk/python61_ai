from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


def fit_linear_regression_gd(
    x: np.ndarray,
    y: np.ndarray,
    learning_rate: float = 0.05,
    epochs: int = 2500,
) -> tuple[float, float, list[float]]:
    w = 0.0
    b = 0.0
    history: list[float] = []

    for _ in range(epochs):
        y_pred = w * x + b
        error = y_pred - y
        loss = float(np.mean(error ** 2))
        history.append(loss)
        dw = float(2 * np.mean(error * x))
        db = float(2 * np.mean(error))
        w -= learning_rate * dw
        b -= learning_rate * db

    return w, b, history


def main() -> None:
    X, y = load_diabetes(return_X_y=True)
    x = X[:, 2]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    w, b, history = fit_linear_regression_gd(x_train, y_train, learning_rate=0.05, epochs=2500)
    gd_pred = w * x_test + b

    sk_model = LinearRegression().fit(x_train.reshape(-1, 1), y_train)
    sk_pred = sk_model.predict(x_test.reshape(-1, 1))

    print("GD coefficients:", round(w, 4), round(b, 4))
    print("GD MAE:", round(mean_absolute_error(y_test, gd_pred), 3))
    print("SK MAE:", round(mean_absolute_error(y_test, sk_pred), 3))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(history, color="teal")
    axes[0].set_title("Loss history")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("MSE")

    axes[1].scatter(x_test, y_test, s=18, alpha=0.7, label="real")
    order = np.argsort(x_test)
    axes[1].plot(x_test[order], gd_pred[order], color="crimson", label="GD")
    axes[1].plot(x_test[order], sk_pred[order], color="royalblue", linestyle="--", label="LinearRegression")
    axes[1].set_title("Predictions on test")
    axes[1].legend()
    plt.tight_layout()
    plt.savefig(Path(__file__).with_suffix('.png'), dpi=120, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()
