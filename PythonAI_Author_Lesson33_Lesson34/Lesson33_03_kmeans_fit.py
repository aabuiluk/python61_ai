"""Пара 33 · завдання 7.2.2: KMeans(n_clusters=4), стовпець cluster_kmeans, центри на графіку.

    python Lesson33_03_kmeans_fit.py
    python Lesson33_03_kmeans_fit.py 2 6       # інші k на тих самих даних (аналог 2.1)
"""

from __future__ import annotations

import sys

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

import clusters as cl


def main() -> None:
    ks = [int(a) for a in sys.argv[1:]] or [4]
    df, y = cl.official_blobs()
    x = df[["x1", "x2"]].to_numpy()

    fig, axes = plt.subplots(1, len(ks), figsize=(5.5 * len(ks), 4.5), squeeze=False)
    for ax, k in zip(axes[0], ks):
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=cl.SEED)
        df[f"cluster_kmeans_{k}" if len(ks) > 1 else "cluster_kmeans"] = kmeans.fit_predict(x)
        labels = kmeans.labels_
        print(f"=== KMeans(n_clusters={k}, random_state=42)")
        print(f"   розміри кластерів: {cl.sizes(labels)}")
        print(f"   cluster_centers_:\n{kmeans.cluster_centers_.round(2)}")
        print(f"   inertia_ (сума квадратів відстаней до свого центру): {kmeans.inertia_:.1f}")
        print(f"   збіг зі справжніми хмарами (ARI): {adjusted_rand_score(y, labels):.3f}\n")
        cl.scatter(ax, x, labels, f"K-Means, k = {k}", kmeans.cluster_centers_)

    print(df.head(3).round(2).to_string())

    if ks == [4]:
        new = np.array([[-8.0, 7.0], [0.0, 0.0], [5.0, 2.0]])
        print("\nНові клієнти: predict призначає найближчий центр, transform дає відстані до всіх 4")
        print(f"   {new.tolist()} → кластери {kmeans.predict(new)}")
        print(kmeans.transform(new).round(2))

    name = "kmeans_clusters.png" if ks == [4] else "kmeans_k_compare.png"
    print(f"\nРисунок: {cl.rel(cl.save(fig, name))}")
    print("K-Means завжди повертає рівно k груп — навіть якщо справжніх хмар інша кількість.")


if __name__ == "__main__":
    main()
