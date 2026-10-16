"""Пара 33 · скільки кластерів: inertia, «лікоть», silhouette — і де K-Means ламається.

    python Lesson33_05_choose_k.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import adjusted_rand_score, silhouette_score

import clusters as cl


def scan(x: np.ndarray, ks) -> tuple[list[float], list[float]]:
    models = [KMeans(n_clusters=k, init="random", n_init=10, random_state=cl.SEED).fit(x) for k in ks]
    return [m.inertia_ for m in models], [silhouette_score(x, m.labels_) for m in models]


def main() -> None:
    ks = range(2, 10)
    x, _ = cl.book_blobs()
    inertias, sils = scan(x, ks)
    print("1) Пʼять згустків з книжки: inertia завжди падає, silhouette має максимум")
    for k, i, s in zip(ks, inertias, sils):
        print(f"   k = {k}: inertia {i:7.1f}   silhouette {s:.3f}")
    print(f"   найкращий silhouette: k = {ks[int(np.argmax(sils))]}")

    df, _ = cl.official_blobs()
    _, sils_official = scan(df.to_numpy(), ks)
    print(f"\n2) Дані ClientScope (практичне 7.2): найкращий silhouette — k = {ks[int(np.argmax(sils_official))]} "
          f"({max(sils_official):.3f})")

    print("\n3) Межі: три еліпси різного розміру")
    x1, y1 = make_blobs(n_samples=1000, centers=((4, -4), (0, 0)), random_state=cl.SEED)
    x1 = x1 @ np.array([[0.374, 0.95], [0.732, 0.598]])   # розтягуємо два згустки
    x2, y2 = make_blobs(n_samples=250, centers=1, random_state=cl.SEED)
    xe, truth = np.r_[x1, x2 + [6, -8]], np.r_[y1, y2 + 2]
    stretched = KMeans(n_clusters=3, n_init=10, random_state=cl.SEED).fit(xe)
    print(f"   збіг K-Means зі справжніми групами (ARI): {adjusted_rand_score(truth, stretched.labels_):.3f}")
    print("   K-Means міряє відстань до центру, тому шукає круглі групи приблизно однакового розміру")

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    axes[0].plot(list(ks), inertias, marker="o")
    axes[0].set_title("inertia: «лікоть» на k = 4")
    axes[1].plot(list(ks), sils, marker="o", color="#e76f51")
    axes[1].set_title("silhouette: максимум на k = 4")
    for ax in axes[:2]:
        ax.set_xlabel("k")
        ax.grid(alpha=0.25)
    cl.scatter(axes[2], xe, stretched.labels_, "Еліпси: K-Means ріже не там", stretched.cluster_centers_)
    print(f"\nРисунок: {cl.rel(cl.save(fig, 'choose_k.png'))}")


if __name__ == "__main__":
    main()
