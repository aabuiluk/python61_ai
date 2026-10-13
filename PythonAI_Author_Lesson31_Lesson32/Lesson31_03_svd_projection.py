"""Пара 31 · крок 3 · завдання 7.1.2: TruncatedSVD(n_components=2) і графік SVD Projection.

Scatter за двома компонентами, колір — сорт вина. Поруч той самий SVD без scaler.

    python Lesson31_03_svd_projection.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

import dimred as dr


def main() -> None:
    features, target = dr.load_wine_frame()
    x = dr.scale(features)
    z, svd = dr.svd_2d(x)

    print(f"1) TruncatedSVD(n_components=2): {x.shape} → {z.shape}")
    print(f"   перші 3 вина в нових координатах:\n{z[:3].round(2)}")
    print(f"   explained_variance_ratio_ = {svd.explained_variance_ratio_.round(3)}, "
          f"разом {svd.explained_variance_ratio_.sum():.1%}")

    fig, ax = plt.subplots(figsize=(6, 4.5))
    dr.scatter(ax, z, target, "SVD Projection", "SVD-1", "SVD-2")
    print(f"   графік: {dr.rel(dr.save(fig, 'svd_projection.png'))}")

    z_raw, svd_raw = dr.svd_2d(features.to_numpy())
    corr = np.corrcoef(z_raw[:, 0], features["proline"])[0, 1]
    print("\n2) Той самий SVD без scaler")
    print(f"   кореляція SVD-1 з однією ознакою proline: {abs(corr):.3f}")
    print("   перша вісь майже дорівнює proline: найбільші числа забрали всю увагу")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    dr.scatter(axes[0], z_raw, target, "SVD без scaler", "SVD-1", "SVD-2")
    dr.scatter(axes[1], z, target, "SVD Projection (після scaler)", "SVD-1", "SVD-2")
    print(f"   графік: {dr.rel(dr.save(fig, 'svd_scaled_vs_raw.png'))}")

    print("\n3) Наскільки добре карта розділяє сорти (kNN на двох координатах, 5-fold)")
    print(f"   без scaler:   {dr.knn_score(z_raw, target):.1%}")
    print(f"   після scaler: {dr.knn_score(z, target):.1%}")
    print(f"   усі 13 ознак: {dr.knn_score(x, target):.1%}")
    print("   SVD сортів не бачив. kNN тут лише лінійка, якою міряємо карту.")

    assert z.shape == (178, 2)
    assert dr.knn_score(z, target) > dr.knn_score(z_raw, target)


if __name__ == "__main__":
    main()
