"""Пара 32 · крок 5 · завдання 7.1.3: PCA(n_components=2) і графік PCA Projection.

Той самий wine і той самий scaler, що на парі 31. Міняємо лише алгоритм.

    python Lesson32_01_pca_projection.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

import dimred as dr


def main() -> None:
    features, target = dr.load_wine_frame()
    x = dr.scale(features)
    p, pca = dr.pca_2d(x)
    ratio = pca.explained_variance_ratio_

    print(f"1) PCA(n_components=2): {x.shape} → {p.shape}")
    print(f"   перші 3 вина:\n{p[:3].round(2)}")
    print(f"   середнє нових координат: {p.mean(axis=0).round(12) + 0.0} — PCA центрує дані")

    print("\n2) explained_variance_ratio_ — частка розкиду таблиці на кожній осі")
    print(f"   PC1 {ratio[0]:.1%} + PC2 {ratio[1]:.1%} = {ratio.sum():.1%}")
    print(f"   решта {1 - ratio.sum():.1%} розкиду на цій карті не видно")
    print(f"   PC1 і PC2 не корелюють: r = {abs(np.corrcoef(p[:, 0], p[:, 1])[0, 1]):.1e}")

    print("\n3) З яких ознак складено осі (pca.components_, три найбільші ваги)")
    for i in range(2):
        top = np.argsort(-np.abs(pca.components_[i]))[:3]
        print(f"   PC{i + 1}: " + ", ".join(f"{features.columns[j]} {pca.components_[i, j]:+.2f}" for j in top))

    fig, ax = plt.subplots(figsize=(6, 4.5))
    dr.scatter(ax, p, target, "PCA Projection", f"PC1 ({ratio[0]:.0%})", f"PC2 ({ratio[1]:.0%})")
    print(f"\n4) Графік: {dr.rel(dr.save(fig, 'pca_projection.png'))}")
    print(f"   сорти на карті (kNN на двох координатах): {dr.knn_score(p, target):.1%}")

    assert p.shape == (178, 2) and np.allclose(p.mean(axis=0), 0)
    assert ratio[0] > ratio[1], "компоненти впорядковано за спаданням дисперсії"


if __name__ == "__main__":
    main()
