"""Пара 5 · графіки розподілу amount (hist + box)."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(Path(__file__).with_name("Lesson5_01_transactions.csv"))
amount = df["amount"].dropna()

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].hist(amount, bins=8, color="steelblue", edgecolor="white")
axes[0].set_title("Hist: amount")
axes[0].set_xlabel("amount")
axes[1].boxplot(amount, vert=True)
axes[1].set_title("Box: amount")
fig.tight_layout()
plt.savefig(Path(__file__).with_suffix(".png"), dpi=120, bbox_inches="tight")
plt.show()
print("n:", len(amount), "median:", round(float(amount.median()), 2))
