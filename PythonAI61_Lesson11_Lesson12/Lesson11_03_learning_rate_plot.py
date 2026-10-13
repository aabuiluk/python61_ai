"""Пара 11 · як learning rate змінює криву loss."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def fit_gd(x: np.ndarray, y: np.ndarray, lr: float, epochs: int = 400) -> list[float]:
    w = b = 0.0
    history: list[float] = []
    for _ in range(epochs):
        err = (w * x + b) - y
        history.append(float(np.mean(err ** 2)))
        w -= lr * float(2 * np.mean(err * x))
        b -= lr * float(2 * np.mean(err))
    return history


rng = np.random.default_rng(42)
x = np.linspace(0, 10, 120)
y = 6.0 * x + 12.0 + rng.normal(0, 8, size=x.shape[0])

fig, ax = plt.subplots(figsize=(8, 4))
for lr in (0.001, 0.01, 0.05):
    ax.plot(fit_gd(x, y, lr), label=f"lr={lr}")
ax.set_title("MSE vs epoch")
ax.set_xlabel("epoch")
ax.set_ylabel("MSE")
ax.legend()
fig.tight_layout()
plt.savefig(Path(__file__).with_suffix(".png"), dpi=120, bbox_inches="tight")
plt.show()
