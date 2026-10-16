"""Спільний код пар 33–34: дані для кластеризації, графіки, оцінка розбиття.

Три набори точок, усі генеруються scikit-learn, інтернет не потрібен:
    official_blobs()  500 точок, 4 хмари — практичне 7.2 ITSTEP (ClientScope)
    book_blobs()      2000 точок, 5 згустків — розділ про кластеризацію в книжці О. Жерона
    moons()           1000 точок, два півмісяці — там, де k-means ламається

Мітки справжніх груп (y) у навчанні не беруть участі: ними лише перевіряємо результат.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # графіки пишемо у файли, вікно не потрібне
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import make_blobs, make_moons

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
SEED = 42
COLORS = ["#2a9d8f", "#e76f51", "#264653", "#e9c46a", "#8338ec", "#3a86ff", "#fb5607", "#6a994e", "#bc4749"]
NOISE = "#b0b0b0"

# Центри і розкид пʼяти згустків — з відкритого коду прикладів книжки (Apache 2.0)
BOOK_CENTERS = np.array([[0.2, 2.3], [-1.5, 2.3], [-2.8, 1.8], [-2.8, 2.8], [-2.8, 1.3]])
BOOK_STD = np.array([0.4, 0.3, 0.1, 0.1, 0.1])


# ---------------------------------------------------------------- дані
def official_blobs() -> tuple[pd.DataFrame, np.ndarray]:
    """Практичне 7.2: make_blobs(n_samples=500, centers=4, cluster_std=1.0, random_state=42)."""
    x, y = make_blobs(n_samples=500, centers=4, cluster_std=1.0, random_state=SEED)
    return pd.DataFrame(x, columns=["x1", "x2"]), y


def book_blobs() -> tuple[np.ndarray, np.ndarray]:
    """2000 точок у пʼяти згустках різної щільності."""
    return make_blobs(n_samples=2000, centers=BOOK_CENTERS, cluster_std=BOOK_STD, random_state=7)


def moons(noise: float = 0.05) -> tuple[np.ndarray, np.ndarray]:
    """Два півмісяці: групи не круглі, тому центр групи нічого не каже про її форму."""
    return make_moons(n_samples=1000, noise=noise, random_state=SEED)


# ---------------------------------------------------------------- підсумки
def sizes(labels) -> str:
    """Розміри груп одним рядком: «0: 125, 1: 125, …, шум: 3»."""
    values, counts = np.unique(np.asarray(labels), return_counts=True)
    parts = [f"{'шум' if v == -1 else v}: {c}" for v, c in zip(values, counts)]
    return ", ".join(parts)


def n_clusters(labels) -> int:
    """Кількість кластерів без шуму (мітка −1 у DBSCAN — не кластер)."""
    return len(set(np.asarray(labels).tolist()) - {-1})


# ---------------------------------------------------------------- графіки
def scatter(ax, x, labels=None, title: str = "", centers=None) -> None:
    """Точки, розфарбовані мітками; −1 (шум) — сірі хрестики; центри — чорні ромби."""
    x = np.asarray(x)
    if labels is None:
        ax.scatter(x[:, 0], x[:, 1], s=12, alpha=0.8, color="0.35")
    else:
        labels = np.asarray(labels)
        for value in np.unique(labels):
            pts = x[labels == value]
            if value == -1:
                ax.scatter(pts[:, 0], pts[:, 1], s=22, marker="x", color=NOISE, label="шум (−1)")
            else:
                ax.scatter(pts[:, 0], pts[:, 1], s=12, alpha=0.85, color=COLORS[int(value) % len(COLORS)],
                           label=f"кластер {value}")
    if centers is not None:
        centers = np.asarray(centers)
        ax.scatter(centers[:, 0], centers[:, 1], s=160, marker="D", color="black", edgecolors="white",
                   linewidths=1.5, label="центри")
    ax.set_title(title)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.grid(alpha=0.25)
    if labels is not None and len(np.unique(labels)) <= 10:
        ax.legend(frameon=False, fontsize=7, loc="best")


def save(fig, name: str) -> Path:
    """Зберігає рисунок у results/ ДО будь-якого plt.show() і закриває його."""
    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / name
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    return out


def rel(path: Path) -> str:
    return str(path.relative_to(HERE))
