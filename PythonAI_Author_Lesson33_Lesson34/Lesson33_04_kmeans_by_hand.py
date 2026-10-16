"""Пара 33 · як працює K-Means: два кроки в циклі і чому важливий старт.

За книжкою О. Жерона: 2000 точок у пʼяти згустках різної щільності.
    крок 1 · кожну точку віддаємо найближчому центру
    крок 2 · кожен центр переносимо в середнє своїх точок
і так доти, доки центри не перестануть рухатись.

    python Lesson33_04_kmeans_by_hand.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

import clusters as cl


def inertia(x: np.ndarray, centers: np.ndarray, labels: np.ndarray) -> float:
    return float((np.linalg.norm(x - centers[labels], axis=1) ** 2).sum())


def main() -> None:
    x, _ = cl.book_blobs()
    k = 5

    print("1) K-Means руками: старт з 5 випадкових точок даних")
    rng = np.random.default_rng(3)
    centers = x[rng.choice(len(x), size=k, replace=False)]
    history = [centers]
    for step in range(1, 100):
        labels = np.linalg.norm(x[:, None, :] - centers[None, :, :], axis=2).argmin(axis=1)
        new = np.array([x[labels == j].mean(axis=0) for j in range(k)])
        moved = np.linalg.norm(new - centers, axis=1).mean()
        if step <= 3:
            print(f"   ітерація {step}: inertia {inertia(x, centers, labels):7.1f}, центри зсунулись у середньому на {moved:.3f}")
        if np.allclose(new, centers):
            break
        centers = new
        history.append(centers)
    print(f"   центри перестали рухатись на ітерації {step}, inertia {inertia(x, centers, labels):.1f}")

    print("\n2) 20 запусків з різним випадковим стартом (init='random', n_init=1)")
    runs = sorted(KMeans(n_clusters=k, init="random", n_init=1, random_state=s).fit(x).inertia_ for s in range(20))
    print(f"   inertia: {[round(r) for r in runs]}")
    best10 = KMeans(n_clusters=k, init="random", n_init=10, random_state=cl.SEED).fit(x).inertia_
    plus = KMeans(n_clusters=k, init="k-means++", n_init=1, random_state=cl.SEED).fit(x).inertia_
    print(f"   n_init=10 лишає найкращий із 10 стартів: {best10:.1f}")
    print(f"   k-means++ (розумний старт) з одного запуску: {plus:.1f}")

    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4.5), sharex=True, sharey=True)
    cl.scatter(left, x, labels, f"Руками: {step} ітерацій", centers)
    path = np.array(history)
    for j in range(k):
        left.plot(path[:, j, 0], path[:, j, 1], color="black", linewidth=1, alpha=0.7)
    worst = KMeans(n_clusters=k, init="random", n_init=1, random_state=int(np.argmax(
        [KMeans(n_clusters=k, init="random", n_init=1, random_state=s).fit(x).inertia_ for s in range(20)]))).fit(x)
    cl.scatter(right, x, worst.labels_, f"Невдалий старт · inertia {worst.inertia_:.0f}", worst.cluster_centers_)
    print(f"\nРисунок: {cl.rel(cl.save(fig, 'kmeans_steps.png'))}")
    print("Чорні лінії — шлях центрів. K-Means знаходить найближчий локальний мінімум, тому стартів кілька.")


if __name__ == "__main__":
    main()
