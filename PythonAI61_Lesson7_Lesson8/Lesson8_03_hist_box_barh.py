"""Пара 8 · hist, box, горизонтальний bar — три типи на одному полотні."""

from pathlib import Path

import matplotlib.pyplot as plt

values = [12, 14, 15, 15, 16, 18, 19, 22, 24, 41]
labels = ["A", "B", "C", "D"]
counts = [9, 15, 7, 12]

fig, axes = plt.subplots(1, 3, figsize=(12, 4))
axes[0].hist(values, bins=5, color="steelblue", edgecolor="white")
axes[0].set_title("hist")
axes[1].boxplot(values)
axes[1].set_title("box (викид 41)")
axes[2].barh(labels, counts, color="darkorange")
axes[2].set_title("barh")
fig.tight_layout()
plt.savefig(Path(__file__).with_suffix(".png"), dpi=120, bbox_inches="tight")
plt.show()
