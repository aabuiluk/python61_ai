"""Пари 31–32 · готова програма: карта вин.

13 хімічних ознак → StandardScaler → PCA → точка на площині. Для вина показує координати,
5 найближчих сусідів на карті і сорт, який вони підказують.

    python Lesson32_05_wine_map.py                      # демо: три вина з таблиці й одне нове
    python Lesson32_05_wine_map.py 0 70 150             # вина за номером рядка (0–177)
    python Lesson32_05_wine_map.py --new alcohol=14.5 proline=1500 flavanoids=3.5
    python Lesson32_05_wine_map.py --features           # назви і середні значення 13 ознак
"""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import dimred as dr

DEMO_NEW = {"alcohol": 14.5, "proline": 1500, "flavanoids": 3.5}


def parse_new(items: list[str], features: pd.DataFrame) -> pd.DataFrame:
    """Нове вино: середні значення всіх ознак, а задані через назва=число — замінюємо."""
    wine = features.mean().to_frame().T
    for item in items:
        name, _, value = item.partition("=")
        if name not in wine.columns:
            raise SystemExit(f"Немає ознаки {name!r}. Список: python Lesson32_05_wine_map.py --features")
        wine[name] = float(value)
    return wine


def describe(label: str, point: np.ndarray, coords: np.ndarray, target: np.ndarray, skip: int | None) -> None:
    dist = np.linalg.norm(coords - point, axis=1)
    if skip is not None:
        dist[skip] = np.inf
    near = np.argsort(dist)[:5]
    votes = np.bincount(target[near], minlength=3)
    print(f"{label}")
    print(f"   на карті: PC1 = {point[0]:+.2f}, PC2 = {point[1]:+.2f}")
    print("   сусіди:   " + ", ".join(f"№{i} (сорт {target[i]})" for i in near))
    print(f"   сусіди підказують сорт {votes.argmax()} ({votes.max()} з 5)\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("wines", nargs="*", type=int, help="номери рядків wine, 0–177")
    parser.add_argument("--new", nargs="+", metavar="ОЗНАКА=ЧИСЛО", help="нове вино: середнє + ваші значення")
    parser.add_argument("--features", action="store_true", help="показати ознаки і вийти")
    args = parser.parse_args()

    features, target = dr.load_wine_frame()
    y = target.to_numpy()
    if args.features:
        print(features.agg(["mean", "min", "max"]).T.round(2).to_string())
        return

    scaler = StandardScaler().fit(features)
    pca = PCA(n_components=2, random_state=dr.SEED).fit(scaler.transform(features))
    coords = pca.transform(scaler.transform(features))
    ratio = pca.explained_variance_ratio_
    print(f"Карта: {features.shape[0]} вин, {features.shape[1]} ознак → 2 осі, "
          f"на них {ratio.sum():.1%} розкиду таблиці (PC1 {ratio[0]:.1%}, PC2 {ratio[1]:.1%})\n")

    demo = not args.wines and not args.new
    marks: list[tuple[str, np.ndarray]] = []
    for i in args.wines or ([0, 70, 150] if demo else []):
        if not 0 <= i < len(features):
            raise SystemExit(f"Номер вина має бути від 0 до {len(features) - 1}")
        describe(f"Вино №{i}, справжній сорт {y[i]}", coords[i], coords, y, skip=i)
        marks.append((f"№{i}", coords[i]))
    if args.new or demo:
        items = args.new or [f"{k}={v}" for k, v in DEMO_NEW.items()]
        wine = parse_new(items, features)
        point = pca.transform(scaler.transform(wine))[0]  # лише transform: осі вже навчені
        describe("Нове вино: середнє, але " + ", ".join(items), point, coords, y, skip=None)
        marks.append(("нове", point))

    fig, ax = plt.subplots(figsize=(7, 5))
    dr.scatter(ax, coords, y, "Карта вин · PCA Projection", f"PC1 ({ratio[0]:.0%})", f"PC2 ({ratio[1]:.0%})")
    for label, point in marks:
        ax.scatter(*point, s=220, facecolors="none", edgecolors="black", linewidths=1.6)
        ax.annotate(label, point, xytext=(8, 8), textcoords="offset points", fontweight="bold")
    print(f"Рисунок: {dr.rel(dr.save(fig, 'wine_map.png'))}")
    if demo:
        print("\nКарта не знає сортів: кольори додано вже після PCA. Нове вино не змінює осей —")
        print("для нього викликаємо лише transform. Наприкінці пари 32 ви знатимете, звідки ці осі.")


if __name__ == "__main__":
    main()
