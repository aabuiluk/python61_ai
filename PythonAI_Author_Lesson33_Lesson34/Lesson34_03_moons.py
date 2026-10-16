"""Пара 34 · півмісяці: де K-Means ламається, а DBSCAN ні. І як DBSCAN-у дати нову точку.

За книжкою О. Жерона: make_moons, 1000 точок.

    python Lesson34_03_moons.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.neighbors import KNeighborsClassifier

import clusters as cl


def main() -> None:
    x, y = cl.moons()

    print("1) Той самий DBSCAN, два eps")
    for eps in (0.05, 0.2):
        model = DBSCAN(eps=eps, min_samples=5).fit(x)
        noise = int((model.labels_ == -1).sum())
        print(f"   eps = {eps}: кластерів {cl.n_clusters(model.labels_)}, "
              f"ядрових точок {len(model.core_sample_indices_)}, шум {noise}")

    kmeans = KMeans(n_clusters=2, n_init=10, random_state=cl.SEED).fit(x)
    dbscan = DBSCAN(eps=0.2, min_samples=5).fit(x)
    print("\n2) Збіг зі справжніми півмісяцями (ARI, 1.0 = ідеально)")
    print(f"   K-Means, k = 2:   {adjusted_rand_score(y, kmeans.labels_):.3f}")
    print(f"   DBSCAN, eps = 0.2: {adjusted_rand_score(y, dbscan.labels_):.3f}")

    print("\n3) У DBSCAN немає predict(). Нову точку віддаємо класифікатору, навченому на ядрових точках")
    knn = KNeighborsClassifier(n_neighbors=50)
    knn.fit(dbscan.components_, dbscan.labels_[dbscan.core_sample_indices_])
    new = np.array([[-0.5, 0], [0, 0.5], [1, -0.1], [2, 1]])
    print(f"   точки {new.tolist()}")
    print(f"   кластери: {knn.predict(new)}")
    dist, idx = knn.kneighbors(new, n_neighbors=1)
    guess = dbscan.labels_[dbscan.core_sample_indices_][idx].ravel()
    guess[dist.ravel() > 0.2] = -1
    print(f"   якщо найближча ядрова точка далі за eps = 0.2 — це шум: {guess}")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharex=True, sharey=True)
    cl.scatter(axes[0], x, kmeans.labels_, "K-Means, k = 2: ріже навпіл", kmeans.cluster_centers_)
    cl.scatter(axes[1], x, dbscan.labels_, "DBSCAN, eps = 0.2: іде за щільністю")
    axes[1].scatter(new[:, 0], new[:, 1], marker="P", s=160, color="black")
    print(f"\nРисунок: {cl.rel(cl.save(fig, 'moons_compare.png'))}")


if __name__ == "__main__":
    main()
