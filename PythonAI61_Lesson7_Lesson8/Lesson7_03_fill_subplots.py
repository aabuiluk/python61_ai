"""Пара 7 · складніше. fill_between + 2×2 subplots."""

from pathlib import Path

import matplotlib.pyplot as plt

hours = [0, 4, 8, 12, 16, 20, 24]
temp = [15, 14, 18, 22, 25, 20, 17]
x = list(range(1, 11))

fig, axes = plt.subplots(2, 2, figsize=(10, 7))
axes[0, 0].plot(x, [v ** 2 for v in x], marker="o")
axes[0, 0].set_title("line")
axes[0, 1].fill_between(hours, temp, color="orange", alpha=0.4)
axes[0, 1].plot(hours, temp, color="darkorange")
axes[0, 1].set_title("fill_between")
axes[1, 0].step(hours, temp, where="mid", color="purple")
axes[1, 0].set_title("step")
axes[1, 1].stem(x, [v ** 2 for v in x], linefmt="C0-", markerfmt="C0o", basefmt="k-")
axes[1, 1].set_title("stem")
fig.suptitle("Кілька видів графіків")
fig.tight_layout()
plt.savefig(Path(__file__).with_suffix(".png"), dpi=120, bbox_inches="tight")
plt.show()
