"""Пара 8 · scatter: зріст / вага."""

from pathlib import Path

import matplotlib.pyplot as plt

height = [160, 165, 170, 175, 180, 185, 190]
weight = [55, 60, 68, 72, 80, 88, 95]

fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(height, weight, s=80, c="teal", alpha=0.85)
ax.set_title("Зріст і вага")
ax.set_xlabel("зріст, см")
ax.set_ylabel("вага, кг")
ax.grid(True, alpha=0.3)
fig.tight_layout()
plt.savefig(Path(__file__).with_suffix(".png"), dpi=120, bbox_inches="tight")
plt.show()
