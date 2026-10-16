"""Пара 34 · завдання 7.2.4: K-Means і DBSCAN в одному вікні, clustering_comparison.png.

    python Lesson34_04_comparison.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

import clusters as cl


def main() -> None:
    df, y = cl.official_blobs()
    x = df[["x1", "x2"]].to_numpy()
    kmeans = KMeans(n_clusters=4, n_init=10, random_state=cl.SEED).fit(x)
    dbscan = DBSCAN(eps=0.8, min_samples=5).fit(x)
    df["cluster_kmeans"] = kmeans.labels_
    df["cluster_dbscan"] = dbscan.labels_

    noise = int((dbscan.labels_ == -1).sum())
    clean = dbscan.labels_ != -1
    print("1) Ті самі 500 точок, два алгоритми")
    print(f"   {'':22}{'K-Means':>10}{'DBSCAN':>10}")
    print(f"   {'кластерів':22}{cl.n_clusters(kmeans.labels_):>10}{cl.n_clusters(dbscan.labels_):>10}")
    print(f"   {'точок у шумі':22}{0:>10}{noise:>10}")
    print(f"   {'збіг із хмарами, ARI':22}{adjusted_rand_score(y, kmeans.labels_):>10.3f}"
          f"{adjusted_rand_score(y, dbscan.labels_):>10.3f}")
    print(f"   {'silhouette':22}{silhouette_score(x, kmeans.labels_):>10.3f}"
          f"{silhouette_score(x[clean], dbscan.labels_[clean]):>10.3f}  (DBSCAN — без шуму)")

    print("\n2) Хто з ким разом: рядки — K-Means, стовпці — DBSCAN")
    print(df.groupby(["cluster_kmeans", "cluster_dbscan"]).size().unstack(fill_value=0).to_string())

    fig = plt.figure(figsize=(11, 4.5))
    ax = plt.subplot(1, 2, 1)
    cl.scatter(ax, x, kmeans.labels_, "K-Means Clustering", kmeans.cluster_centers_)
    ax = plt.subplot(1, 2, 2)
    cl.scatter(ax, x, dbscan.labels_, "DBSCAN Clustering")
    print(f"\nРисунок: {cl.rel(cl.save(fig, 'clustering_comparison.png'))}")
    print("На круглих хмарах однакової щільності обидва бачать ті самі 4 групи. DBSCAN додатково")
    print("позначає крайніх клієнтів як шум — K-Means таких не має: він віддає кожну точку якомусь центру.")


if __name__ == "__main__":
    main()
