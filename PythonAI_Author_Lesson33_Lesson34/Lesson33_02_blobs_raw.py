"""Пара 33 · завдання 7.2.1: дані ClientScope як make_blobs і сирий scatter.

500 «клієнтів» з двома ознаками, згенерованих навколо 4 центрів. Номер справжньої хмари y
алгоритм не побачить: ним лише перевіримо результат наприкінці пари.

    python Lesson33_02_blobs_raw.py
    python Lesson33_02_blobs_raw.py 2.5      # cluster_std: розкид кожної хмари (аналог 1.1)
"""

from __future__ import annotations

import sys

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import make_blobs

import clusters as cl


def main() -> None:
    std = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    x, y = make_blobs(n_samples=500, centers=4, cluster_std=std, random_state=cl.SEED)
    df = pd.DataFrame(x, columns=["x1", "x2"])

    print(f"1) make_blobs(n_samples=500, centers=4, cluster_std={std}, random_state=42)")
    print(f"   DataFrame {df.shape}: ознаки x1, x2. Справжні хмари y лежать окремо, у таблицю не йдуть.")
    print(df.head(3).round(2).to_string())

    print("\n2) Що видно до будь-якої моделі")
    print(df.describe().loc[["mean", "std", "min", "max"]].round(2).to_string())

    fig, ax = plt.subplots(figsize=(6, 4.5))
    cl.scatter(ax, df.to_numpy(), None, f"Сирі точки · cluster_std = {std}")
    print(f"\nРисунок: {cl.rel(cl.save(fig, 'raw_blobs.png'))}")
    print("Кольорів немає: групи на око шукаєте ви. Наступний крок — нехай їх шукає K-Means.")


if __name__ == "__main__":
    main()
