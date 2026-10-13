"""Пара 32 · крок 6: PCA руками і чим він відрізняється від SVD.

PCA = відняти середнє → матриця коваріацій → власні вектори. Те саме дає SVD центрованої таблиці.
Тому після StandardScaler SVD і PCA збігаються, а без центрування — ні.

    python Lesson32_02_pca_by_hand.py
"""

from __future__ import annotations

import numpy as np

import dimred as dr


def main() -> None:
    np.set_printoptions(precision=3, suppress=True)
    features, _ = dr.load_wine_frame()
    x = dr.scale(features)
    n = len(x)

    centered = x - x.mean(axis=0)
    cov = centered.T @ centered / (n - 1)
    values, vectors = np.linalg.eigh(cov)
    order = np.argsort(-values)
    values, vectors = values[order], vectors[:, order]
    p_hand = centered @ vectors[:, :2]
    print("1) PCA руками")
    print(f"   матриця коваріацій {cov.shape}, власні числа: {values[:4].round(2)} …")
    print(f"   частка кожного: {(values / values.sum())[:4].round(3)} …")

    p, pca = dr.pca_2d(x)
    print("\n2) Порівняння з sklearn.decomposition.PCA")
    print(f"   explained_variance_ratio_: {pca.explained_variance_ratio_.round(3)}")
    print(f"   різниця координат: {np.abs(p - dr.align_signs(p, p_hand)).max():.1e}")

    _, s, vt = np.linalg.svd(centered, full_matrices=False)
    print("\n3) Той самий PCA через SVD центрованої таблиці")
    print(f"   s² / (n − 1) = {(s ** 2 / (n - 1))[:4].round(2)} — це власні числа з кроку 1")
    print(f"   різниця осей: {np.abs(np.abs(vt[:2]) - np.abs(pca.components_)).max():.1e}")

    z, _ = dr.svd_2d(x)
    print("\n4) TruncatedSVD проти PCA на масштабованому wine")
    print(f"   різниця координат: {np.abs(p - dr.align_signs(p, z)).max():.1e}")
    print("   StandardScaler уже відняв середнє, тому PCA більше нічого центрувати")

    raw = features.to_numpy()
    z_raw, svd_raw = dr.svd_2d(raw)
    p_raw, pca_raw = dr.pca_2d(raw)
    mean = raw.mean(axis=0)
    cos = abs(svd_raw.components_[0] @ mean) / np.linalg.norm(mean)
    print("\n5) Те саме без scaler (дані не центровані)")
    print(f"   різниця координат SVD і PCA: {np.abs(p_raw - dr.align_signs(p_raw, z_raw)).max():.0f}")
    print(f"   косинус між першою віссю SVD і вектором середніх: {cos:.4f}")
    print("   перша вісь SVD показує, де лежить хмара відносно нуля, а не як вона розкидана")
    print(f"   SVD-1: від {z_raw[:, 0].min():.0f} до {z_raw[:, 0].max():.0f};  "
          f"PC1: від {p_raw[:, 0].min():.0f} до {p_raw[:, 0].max():.0f}")

    assert np.allclose(values[:2] / values.sum(), pca.explained_variance_ratio_)
    assert np.allclose(p, dr.align_signs(p, p_hand)) and np.allclose(p, dr.align_signs(p, z), atol=1e-6)
    print("\nPCA = центрування + SVD. Знак осі довільний: графік може бути дзеркальним, і це не помилка.")


if __name__ == "__main__":
    main()
