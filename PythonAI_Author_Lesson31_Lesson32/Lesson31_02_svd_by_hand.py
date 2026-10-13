"""Пара 31 · крок 2: SVD-розклад руками на numpy.

X = U · S · Vᵀ. Залишаємо k найбільших сингулярних чисел — отримуємо найкраще наближення рангу k.
Нові координати рядків: Z = U_k · S_k = X · V_k.

    python Lesson31_02_svd_by_hand.py
"""

from __future__ import annotations

import numpy as np
from sklearn.decomposition import TruncatedSVD

import dimred as dr


def main() -> None:
    np.set_printoptions(precision=2, suppress=True)
    a = np.array([[5.0, 4.0, 1.0], [4.0, 5.0, 1.0], [1.0, 1.0, 5.0], [2.0, 1.0, 4.0]])
    u, s, vt = np.linalg.svd(a, full_matrices=False)
    print("1) Маленька таблиця 4 × 3 (4 покупці оцінили 3 товари)")
    print(a)
    print(f"   U {u.shape}, S {s.round(2)}, Vᵀ {vt.shape}")
    print(f"   U·S·Vᵀ повертає таблицю: похибка {np.abs(u * s @ vt - a).max():.1e}")

    print("\n2) Залишаємо k найбільших сингулярних чисел")
    for k in (1, 2):
        approx = u[:, :k] * s[:k] @ vt[:k]
        err = np.linalg.norm(a - approx)
        print(f"   k={k}: похибка {err:.2f} = корінь із суми відкинутих s² = {np.sqrt((s[k:] ** 2).sum()):.2f}")
    print("   наближення рангу 2:")
    print(u[:, :2] * s[:2] @ vt[:2])
    print("   нові координати рядків Z = U·S (4 × 2):")
    print(u[:, :2] * s[:2])

    features, _ = dr.load_wine_frame()
    x = dr.scale(features)
    u, s, vt = np.linalg.svd(x, full_matrices=False)
    energy = s ** 2 / (s ** 2).sum()
    print(f"\n3) Wine після scaler: {x.shape}, сингулярних чисел {len(s)}")
    print(f"   s  = {s[:5].round(1)} …")
    print(f"   частка s² = {energy[:5].round(3)} …")

    z_hand = u[:, :2] * s[:2]
    z_proj = x @ vt[:2].T
    z_sklearn = TruncatedSVD(n_components=2, algorithm="arpack").fit_transform(x)
    z_sklearn = dr.align_signs(z_hand, z_sklearn)
    print("\n4) Дві компоненти трьома способами")
    print(f"   U·S і X·V збігаються:            {np.abs(z_hand - z_proj).max():.1e}")
    print(f"   numpy і TruncatedSVD збігаються: {np.abs(z_hand - z_sklearn).max():.1e}  (з точністю до знака осі)")

    print("\n5) Скільки таблиці зберігає k компонент")
    print("    k   частка s²   відносна похибка відновлення")
    for k in (1, 2, 3, 5, 8, 13):
        approx = u[:, :k] * s[:k] @ vt[:k]
        print(f"   {k:>2}   {energy[:k].sum():>8.1%}   {np.linalg.norm(x - approx) / np.linalg.norm(x):>8.1%}")

    print("\n6) З чого складаються нові осі (три найбільші ваги)")
    for i in range(2):
        top = np.argsort(-np.abs(vt[i]))[:3]
        print(f"   SVD-{i + 1}: " + ", ".join(f"{features.columns[j]} {vt[i, j]:+.2f}" for j in top))

    assert np.allclose(z_hand, z_proj) and np.allclose(z_hand, z_sklearn, atol=1e-6)
    assert np.isclose(energy.sum(), 1.0)
    print("\nДві компоненти — це не два початкові стовпці, а дві суміші всіх 13.")


if __name__ == "__main__":
    main()
