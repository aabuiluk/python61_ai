"""Пара 32 · крок 7 · завдання 7.1.4: SVD і PCA поруч в одному вікні.

Два subplot з підписами SVD Projection і PCA Projection, друк explained_variance_ratio_,
підсумковий файл dimensionality_reduction_comparison.png.

    python Lesson32_03_svd_vs_pca.py
    python Lesson32_03_svd_vs_pca.py --raw      # третій рядок: те саме без scaler
"""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

import dimred as dr


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", action="store_true", help="додати порівняння без scaler")
    args = parser.parse_args()

    features, target = dr.load_wine_frame()
    x = dr.scale(features)
    z, svd = dr.svd_2d(x)
    p, pca = dr.pca_2d(x)
    ratio = pca.explained_variance_ratio_

    print("1) Один X після scaler, два алгоритми")
    print(f"   PCA explained_variance_ratio_ = {ratio.round(4)}, сума {ratio.sum():.4f}")
    print(f"   SVD explained_variance_ratio_ = {svd.explained_variance_ratio_.round(4)}, "
          f"сума {svd.explained_variance_ratio_.sum():.4f}")

    flipped = [i + 1 for i in range(2) if (z[:, i] * p[:, i]).sum() < 0]
    diff = np.abs(p - dr.align_signs(p, z)).max()
    print("\n2) Наскільки різні координати")
    print(f"   найбільша різниця після вирівнювання знаків: {diff:.1e}")
    print(f"   дзеркальні осі: {', '.join(map(str, flipped)) or 'немає'}")

    rows = 2 if args.raw else 1
    fig, axes = plt.subplots(rows, 2, figsize=(11, 4.5 * rows), squeeze=False)
    dr.scatter(axes[0, 0], z, target, "SVD Projection", "SVD-1", "SVD-2")
    dr.scatter(axes[0, 1], p, target, "PCA Projection", f"PC1 ({ratio[0]:.0%})", f"PC2 ({ratio[1]:.0%})")
    print("\n3) Якість карти (kNN на двох координатах, 5-fold)")
    print(f"   SVD після scaler: {dr.knn_score(z, target):.1%}")
    print(f"   PCA після scaler: {dr.knn_score(p, target):.1%}")
    if args.raw:
        raw = features.to_numpy()
        z_raw, _ = dr.svd_2d(raw)
        p_raw, pca_raw = dr.pca_2d(raw)
        dr.scatter(axes[1, 0], z_raw, target, "SVD без scaler", "SVD-1", "SVD-2")
        dr.scatter(axes[1, 1], p_raw, target, "PCA без scaler", "PC1", "PC2")
        print(f"   SVD без scaler:   {dr.knn_score(z_raw, target):.1%}")
        print(f"   PCA без scaler:   {dr.knn_score(p_raw, target):.1%}")
        print(f"   PCA без scaler «пояснює» {pca_raw.explained_variance_ratio_.sum():.2%} дисперсії — "
              "але це дисперсія одного proline")
    fig.tight_layout()
    out = dr.save(fig, "dimensionality_reduction_comparison.png")
    print(f"\n4) Підсумковий рисунок: {dr.rel(out)}")
    print("   Графіки однакові — це не помилка. Після scaler дані центровані, а PCA = центрування + SVD.")

    assert diff < 1e-6


if __name__ == "__main__":
    main()
