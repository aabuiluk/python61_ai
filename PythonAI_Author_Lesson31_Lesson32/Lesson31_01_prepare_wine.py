"""Пара 31 · крок 1 · завдання 7.1.1: таблиця wine і StandardScaler.

load_wine → pandas.DataFrame → розмір матриці ознак → масштаби стовпців → z-score.

    python Lesson31_01_prepare_wine.py
"""

from __future__ import annotations

import numpy as np

import dimred as dr


def main() -> None:
    features, target = dr.load_wine_frame()
    df = features.copy()
    df["target"] = target

    print(f"1) DataFrame {df.shape}: 13 ознак + стовпець target. Матриця ознак X — {features.shape}")
    print("   сортів: " + ", ".join(f"{cls} → {n} вин" for cls, n in target.value_counts().sort_index().items()))
    print(df.iloc[:3, [0, 1, 9, 10, 12, 13]].to_string(index=False))

    stats = features.agg(["mean", "std", "min", "max"]).T.sort_values("std", ascending=False)
    print("\n2) Масштаби ознак дуже різні (від найбільшого розкиду до найменшого)")
    print(stats.iloc[[0, 1, 2, -2, -1]].round(2).to_string())
    share = features.var() / features.var().sum()
    print(f"   proline дає {share['proline']:.1%} усієї дисперсії таблиці — лише через одиниці вимірювання.")

    x = dr.scale(features)
    print("\n3) Після StandardScaler кожен стовпець має середнє 0 і розкид 1")
    print(f"   середнє по стовпцях: від {x.mean(axis=0).min():.1e} до {x.mean(axis=0).max():.1e}")
    print(f"   std по стовпцях:     від {x.std(axis=0).min():.3f} до {x.std(axis=0).max():.3f}")
    print(f"   тепер кожна ознака дає {1 / x.shape[1]:.1%} дисперсії — усі «звучать» однаково гучно")

    col = features["proline"].to_numpy()
    by_hand = (col - col.mean()) / col.std()
    print("\n4) z-score руками: (x − mean) / std")
    print(f"   proline[0] = {col[0]:.0f}, mean = {col.mean():.1f}, std = {col.std():.1f} → z = {by_hand[0]:.3f}")
    print(f"   scaler дав {x[0, -1]:.3f}")

    assert x.shape == (178, 13), "у X не має бути стовпця target"
    assert np.allclose(x.mean(axis=0), 0) and np.allclose(x.std(axis=0), 1)
    assert np.allclose(by_hand, x[:, -1])
    print("\nПастка: якщо залишити target у X, SVD отримає відповідь як ще одну ознаку.")
    print("Сорт потрібен лише для кольору точок на графіку.")


if __name__ == "__main__":
    main()
