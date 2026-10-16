"""Пара 34 · завдання 7.2.3: DBSCAN(eps=0.8, min_samples=5), стовпець cluster_dbscan, шум −1.

DBSCAN не питає кількість кластерів. Він питає, що вважати «густо»:
    eps          радіус сусідства
    min_samples  скільки точок (разом із самою точкою) має бути в цьому радіусі

    python Lesson34_01_dbscan.py
    python Lesson34_01_dbscan.py 0.3 2.0       # інші eps на тих самих даних (аналог 3.1)
"""

from __future__ import annotations

import sys

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN

import clusters as cl


def kinds(model: DBSCAN) -> tuple[int, int, int]:
    """Скільки точок ядрових, межових і шумових."""
    core = np.zeros(len(model.labels_), dtype=bool)
    core[model.core_sample_indices_] = True
    noise = model.labels_ == -1
    return int(core.sum()), int((~core & ~noise).sum()), int(noise.sum())


def main() -> None:
    eps_list = [float(a) for a in sys.argv[1:]] or [0.8]
    df, _ = cl.official_blobs()
    x = df[["x1", "x2"]].to_numpy()

    fig, axes = plt.subplots(1, len(eps_list), figsize=(5.5 * len(eps_list), 4.5), squeeze=False)
    for ax, eps in zip(axes[0], eps_list):
        model = DBSCAN(eps=eps, min_samples=5).fit(x)
        labels = model.labels_
        column = "cluster_dbscan" if len(eps_list) == 1 else f"cluster_dbscan_{eps}"
        df[column] = labels
        core, border, noise = kinds(model)
        print(f"=== DBSCAN(eps={eps}, min_samples=5)")
        print(f"   кластерів: {cl.n_clusters(labels)}, шум (−1): {noise} з {len(x)} ({noise / len(x):.0%})")
        print(f"   ядрових точок {core}, межових {border}, шумових {noise}")
        print(f"   розміри: {cl.sizes(labels)}\n")
        cl.scatter(ax, x, labels, f"DBSCAN, eps = {eps}: {cl.n_clusters(labels)} кл., шум {noise}")

    print(df.head(3).round(2).to_string())
    name = "dbscan_clusters.png" if len(eps_list) == 1 else "dbscan_eps_compare.png"
    print(f"\nРисунок: {cl.rel(cl.save(fig, name))}")
    print("Мітка −1 — це «шум»: точка не потрапила в жодну густу область. Це не ще один кластер.")


if __name__ == "__main__":
    main()
