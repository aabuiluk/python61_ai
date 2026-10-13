from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def main() -> None:
    X, y = load_diabetes(return_X_y=True)
    x = X[:, 2].reshape(-1, 1)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model = LinearRegression().fit(x_train, y_train)
    y_pred = model.predict(x_test)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(x_test, y_test, alpha=0.7, label="реальні y")
    order = np.argsort(x_test.ravel())
    ax.plot(x_test[order], y_pred[order], color="crimson", linewidth=2, label="регресія")
    ax.set_xlabel("ознака x")
    ax.set_ylabel("цільова y")
    ax.set_title("Одна ознака + лінійна регресія")
    ax.legend()
    plt.tight_layout()
    plt.savefig(Path(__file__).with_suffix('.png'), dpi=120, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()
