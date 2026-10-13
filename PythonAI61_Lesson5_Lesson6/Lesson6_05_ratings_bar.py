"""Пара 6 · стовпчикова діаграма частот рейтингу."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(Path(__file__).with_name("Lesson6_01_ratings.csv"))
freq = df["rating"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(freq.index.astype(str), freq.values, color="teal")
ax.set_title("Частота рейтингів")
ax.set_xlabel("rating")
ax.set_ylabel("count")
fig.tight_layout()
plt.savefig(Path(__file__).with_suffix(".png"), dpi=120, bbox_inches="tight")
plt.show()
print(freq)
