from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def main() -> None:
    X, y = load_diabetes(return_X_y=True)
    x = X[:, 2]
    x_train, _, y_train, _ = train_test_split(x, y, test_size=0.2, random_state=42)

    b = float(np.mean(y_train))
    weights = np.linspace(-80, 80, 160)
    losses = [float(np.mean(((w * x_train + b) - y_train) ** 2)) for w in weights]

    best_w = float(weights[int(np.argmin(losses))])
    sk_w = float(LinearRegression().fit(x_train.reshape(-1, 1), y_train).coef_[0])

    plt.plot(weights, losses, color="teal", label="MSE(w)")
    plt.axvline(best_w, color="crimson", linestyle="--", label=f"grid min w={best_w:.2f}")
    plt.axvline(sk_w, color="royalblue", linestyle=":", label=f"sklearn w={sk_w:.2f}")
    plt.xlabel("w")
    plt.ylabel("MSE")
    plt.title("Loss як функція від w")
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path(__file__).with_suffix('.png'), dpi=120, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()
