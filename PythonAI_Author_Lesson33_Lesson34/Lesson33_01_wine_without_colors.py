"""Пара 33 · місток з пар 31–32: карта вин без кольорів.

На парі 32 три сорти на карті PCA було видно, бо ми самі розфарбували точки за target.
Тепер кольорів немає: K-Means отримує лише 178 точок на площині і сам ділить їх на 3 групи.
Потім — уже після навчання — порівнюємо групи із сортами.

    python Lesson33_01_wine_without_colors.py
    python Lesson33_01_wine_without_colors.py 4        # інша кількість кластерів
"""

from __future__ import annotations

import sys

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score
from sklearn.preprocessing import StandardScaler

import clusters as cl


def main() -> None:
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    wine = load_wine(as_frame=True)
    features, target = wine.data, wine.target.to_numpy()

    pca = PCA(n_components=2, random_state=cl.SEED)
    coords = pca.fit_transform(StandardScaler().fit_transform(features))
    print(f"1) Карта з пари 32: {features.shape} → {coords.shape}, "
          f"на двох осях {pca.explained_variance_ratio_.sum():.1%} розкиду")

    kmeans = KMeans(n_clusters=k, n_init=10, random_state=cl.SEED)
    labels = kmeans.fit_predict(coords)          # target сюди не передаємо
    print(f"\n2) KMeans(n_clusters={k}) на тих самих 178 точках, без кольорів")
    print(f"   розміри груп: {cl.sizes(labels)}")
    print(f"   центри груп на карті:\n{kmeans.cluster_centers_.round(2)}")

    print("\n3) Лише тепер дивимось на сорти: скільки вин кожного сорту потрапило в кожну групу")
    table = pd.crosstab(pd.Series(target, name="сорт"), pd.Series(labels, name="кластер"))
    print(table.to_string())
    print(f"   узгодженість із сортами (ARI, 1.0 = ідеально): {adjusted_rand_score(target, labels):.3f}")

    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4.5), sharex=True, sharey=True)
    cl.scatter(left, coords, target, "Пара 32: колір — справжній сорт")
    cl.scatter(right, coords, labels, f"Пара 33: колір — кластер K-Means, k = {k}", kmeans.cluster_centers_)
    for ax in (left, right):
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
    print(f"\nРисунок: {cl.rel(cl.save(fig, 'wine_without_colors.png'))}")
    print("\nНомери кластерів довільні: кластер 0 не мусить бути сортом 0. Важить лише, хто з ким разом.")


if __name__ == "__main__":
    main()
