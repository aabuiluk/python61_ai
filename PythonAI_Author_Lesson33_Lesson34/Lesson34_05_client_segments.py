"""Пари 33–34 · готова програма: сегменти клієнтів ClientScope.

Дані синтетичні: 500 клієнтів з практичного 7.2 (make_blobs), дві ознаки переведено в зрозумілі
одиниці — витрати на місяць (грн) і візити на місяць. Програма масштабує ознаки, ділить клієнтів
K-Means і DBSCAN, друкує профіль кожного сегмента і показує, куди потрапить новий клієнт.

    python Lesson34_05_client_segments.py
    python Lesson34_05_client_segments.py --new spend=900 visits=10
    python Lesson34_05_client_segments.py --k 3 --eps 0.3
"""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler

import clusters as cl


def clients() -> pd.DataFrame:
    """Ті самі 500 точок, лише в одиницях бізнесу: spend = 100·x1 + 1500, visits = x2 + 10."""
    df, _ = cl.official_blobs()
    return pd.DataFrame({"spend": (100 * df["x1"] + 1500).round(0), "visits": (df["x2"] + 10).round(1)})


def profile(data: pd.DataFrame, labels, name: str) -> None:
    table = data.assign(segment=labels).groupby("segment").agg(
        clients=("spend", "size"), spend=("spend", "mean"), visits=("visits", "mean")).round(1)
    table.index = ["шум" if i == -1 else i for i in table.index]
    print(f"--- {name}\n{table.to_string()}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=4, help="кількість сегментів для K-Means")
    parser.add_argument("--eps", type=float, default=0.15, help="eps для DBSCAN на масштабованих ознаках")
    parser.add_argument("--new", nargs="+", metavar="ОЗНАКА=ЧИСЛО", help="новий клієнт: spend=… visits=…")
    args = parser.parse_args()

    data = clients()
    scaler = StandardScaler().fit(data)
    z = scaler.transform(data)
    kmeans = KMeans(n_clusters=args.k, n_init=10, random_state=cl.SEED).fit(z)
    dbscan = DBSCAN(eps=args.eps, min_samples=5).fit(z)
    print(f"Клієнтів: {len(data)}; ознаки spend (грн/міс) і visits (разів/міс) масштабовано StandardScaler\n")
    profile(data, kmeans.labels_, f"K-Means, k = {args.k}")
    profile(data, dbscan.labels_, f"DBSCAN, eps = {args.eps} (у масштабованих одиницях)")

    point = None
    if args.new:
        new = data.mean().to_frame().T
        for item in args.new:
            name, _, value = item.partition("=")
            if name not in new.columns:
                raise SystemExit(f"Ознаки: spend, visits. Немає {name!r}")
            new[name] = float(value)
        point = scaler.transform(new)
        segment = int(kmeans.predict(point)[0])
        dist = np.linalg.norm(dbscan.components_ - point, axis=1)
        nearest = int(dist.argmin())
        dense = dbscan.labels_[dbscan.core_sample_indices_][nearest] if dist[nearest] <= args.eps else -1
        print(f"Новий клієнт: spend={new['spend'][0]:.0f}, visits={new['visits'][0]:.1f}")
        print(f"   K-Means: сегмент {segment} (найближчий центр)")
        print(f"   DBSCAN:  {'шум — поруч немає густої групи' if dense == -1 else f'сегмент {dense}'}"
              f" (до найближчого ядрового клієнта {dist[nearest]:.2f})\n")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharex=True, sharey=True)
    centers = scaler.inverse_transform(kmeans.cluster_centers_)
    cl.scatter(axes[0], data.to_numpy(), kmeans.labels_, f"K-Means, k = {args.k}", centers)
    cl.scatter(axes[1], data.to_numpy(), dbscan.labels_, f"DBSCAN, eps = {args.eps}")
    for ax in axes:
        ax.set_xlabel("spend, грн на місяць")
        ax.set_ylabel("visits на місяць")
        if point is not None:
            raw = scaler.inverse_transform(point)[0]
            ax.scatter(*raw, marker="*", s=380, color="black")
    print(f"Рисунок: {cl.rel(cl.save(fig, 'client_segments.png'))}")
    print("Номери сегментів самі нічого не означають. Зміст дає таблиця профілю: хто платить більше, хто ходить частіше.")


if __name__ == "__main__":
    main()
