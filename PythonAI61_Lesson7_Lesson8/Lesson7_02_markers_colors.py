"""Пара 7 · легко/середнє. Кілька ліній: колір, маркер, стиль."""

from pathlib import Path

import matplotlib.pyplot as plt

x = list(range(1, 9))
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, [v for v in x], color="royalblue", marker="o", label="y = x")
ax.plot(x, [v ** 2 for v in x], color="crimson", marker="s", linestyle="--", label="y = x²")
ax.plot(x, [v ** 0.5 * 4 for v in x], color="seagreen", marker="^", linestyle=":", label="≈ √x")
ax.set_title("Одна вісь, різні стилі")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
plt.savefig(Path(__file__).with_suffix(".png"), dpi=120, bbox_inches="tight")
plt.show()
