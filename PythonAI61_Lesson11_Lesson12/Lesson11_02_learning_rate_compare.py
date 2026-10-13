import numpy as np


def fit_gd(x: np.ndarray, y: np.ndarray, learning_rate: float, epochs: int = 400) -> list[float]:
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

    return history


def main() -> None:
    rng = np.random.default_rng(42)
    x = np.linspace(0, 10, 120)
    y = 6.0 * x + 12.0 + rng.normal(0, 8, size=x.shape[0])

    for lr in (0.001, 0.01, 0.1):
        history = fit_gd(x, y, learning_rate=lr)
        print(f"lr={lr}: start={history[0]:.2f}, mid={history[len(history)//2]:.2f}, end={history[-1]:.2f}")


if __name__ == "__main__":
    main()
