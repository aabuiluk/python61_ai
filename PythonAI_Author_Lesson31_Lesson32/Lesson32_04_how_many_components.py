"""Пара 32 · крок 8: скільки компонент лишати і PCA перед класифікацією.

Scree plot, накопичена частка дисперсії, а потім Pipeline: scaler → PCA(k) → LogisticRegression.

    python Lesson32_04_how_many_components.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import dimred as dr


def main() -> None:
    features, target = dr.load_wine_frame()
    x = dr.scale(features)
    ratio = PCA().fit(x).explained_variance_ratio_
    total = np.cumsum(ratio)

    print("1) Усі 13 компонент: частка дисперсії і накопичена сума")
    for k in range(1, 14):
        print(f"   PC{k:<2} {ratio[k - 1]:>6.1%}  разом {total[k - 1]:>6.1%}  {'█' * round(ratio[k - 1] * 60)}")

    print("\n2) Скільки компонент треба, щоб зберегти задану частку")
    for level in (0.80, 0.90, 0.95):
        print(f"   {level:.0%} → {int(np.searchsorted(total, level) + 1)} компонент")
    auto = PCA(n_components=0.90).fit(x)
    print(f"   PCA(n_components=0.90) сам вибрав {auto.n_components_}")

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ks = np.arange(1, 14)
    ax.bar(ks, ratio, color=dr.COLORS[0], label="частка компоненти")
    ax.plot(ks, total, marker="o", color=dr.COLORS[1], label="накопичена сума")
    ax.axhline(0.9, linestyle="--", color="gray", linewidth=1)
    ax.set_xticks(ks)
    ax.set_xlabel("номер компоненти")
    ax.set_ylabel("частка дисперсії")
    ax.set_title("Scree plot · wine")
    ax.legend(frameon=False)
    print(f"   графік: {dr.rel(dr.save(fig, 'scree_plot.png'))}")

    print("\n3) PCA як крок перед класифікацією (LogisticRegression, 5-fold)")
    cv = StratifiedKFold(5, shuffle=True, random_state=dr.SEED)
    raw = features.to_numpy()
    print("    k   точність")
    for k in (1, 2, 3, 5, 8, 13):
        model = make_pipeline(StandardScaler(), PCA(n_components=k), LogisticRegression(max_iter=2000))
        print(f"   {k:>2}   {cross_val_score(model, raw, target, cv=cv).mean():.1%}")
    plain = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    print(f"   без PCA: {cross_val_score(plain, raw, target, cv=cv).mean():.1%}")

    print("\nScaler і PCA стоять усередині Pipeline: у кожному fold вони навчаються лише на train-частині.")
    print("Якщо зробити fit_transform на всій таблиці до поділу, тестові рядки вплинуть на осі — це leakage.")
    print("Сорт вина бачить тільки LogisticRegression. PCA шукає осі без нього.")


if __name__ == "__main__":
    main()
