"""Пара 34 · як вибрати eps: графік k-відстаней і чому без масштабу eps — лотерея.

Для кожної точки беремо відстань до її min_samples-го сусіда і сортуємо. Поки точка всередині
густої хмари, ця відстань мала; на шумі вона різко росте. Місце злому — розумний eps.

    python Lesson34_02_choose_eps.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

import clusters as cl

MIN_SAMPLES = 5


def k_distances(x: np.ndarray) -> np.ndarray:
    dist, _ = NearestNeighbors(n_neighbors=MIN_SAMPLES).fit(x).kneighbors(x)
    return np.sort(dist[:, -1])   # відстань до 5-ї точки, рахуючи саму точку


def main() -> None:
    df, _ = cl.official_blobs()
    x = df.to_numpy()
    kd = k_distances(x)
    print("1) Відстань до 5-го сусіда, відсортована")
    for q in (50, 90, 95, 99, 100):
        print(f"   {q:>3}-й перцентиль: {np.percentile(kd, q):.2f}")

    print("\n2) eps навколо злому графіка")
    for eps in (0.3, 0.5, 0.8, 1.2, 2.0, 4.0):
        labels = DBSCAN(eps=eps, min_samples=MIN_SAMPLES).fit_predict(x)
        print(f"   eps = {eps:<4}: кластерів {cl.n_clusters(labels)}, шум {int((labels == -1).sum()):3d}")

    print("\n3) Масштаб: ознаку x2 записали в інших одиницях (× 100)")
    stretched = x * [1, 100]
    labels = DBSCAN(eps=0.8, min_samples=MIN_SAMPLES).fit_predict(stretched)
    print(f"   той самий eps = 0.8: кластерів {cl.n_clusters(labels)}, шум {int((labels == -1).sum())} з {len(x)}")
    print("   DBSCAN міряє відстані, тому ознаки в різних одиницях масштабують перед ним — як перед PCA на парі 31")

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.plot(kd)
    ax.axhline(0.8, color="#e76f51", linestyle="--", label="eps = 0.8 з практичного")
    ax.set_xlabel("точки, відсортовані за відстанню")
    ax.set_ylabel(f"відстань до {MIN_SAMPLES}-го сусіда")
    ax.set_title("Графік k-відстаней: eps — там, де крива злітає")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    print(f"\nРисунок: {cl.rel(cl.save(fig, 'k_distance.png'))}")


if __name__ == "__main__":
    main()
