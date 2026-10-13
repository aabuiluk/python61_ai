"""Чотири конфіги, одна таблиця, PNG, state_dict переможця."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import torch

from data import load_tensors, set_seeds
from evaluate import test_metrics
from models import CONFIGS, MLP
from train import train

OUT = Path(__file__).resolve().parent


def main() -> None:
    set_seeds()
    data = load_tensors()
    rows: list[tuple[str, float, float, float, list[float], MLP]] = []
    for name, use_bn, dropout_p in CONFIGS:
        model = MLP(use_bn=use_bn, dropout_p=dropout_p)
        history = train(model, data)
        mae, r2, gap = test_metrics(model, data)
        rows.append((name, mae, r2, gap, history, model))
        print(f"{name:<18} MAE={mae:.3f}  R2={r2:.3f}  train−test MAE={gap:.3f}")

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    for name, _mae, _r2, _gap, history, _model in rows:
        ax.plot(range(1, len(history) + 1), history, label=name)
    ax.set_xlabel("епоха")
    ax.set_ylabel("train MSE")
    ax.legend()
    ax.grid(True, alpha=0.3)
    png = OUT / "loss_curve.png"
    fig.tight_layout()
    fig.savefig(png, dpi=120)
    plt.close(fig)

    winner_name, _mae, _r2, _gap, _hist, winner = min(rows, key=lambda row: row[1])
    weights = OUT / "winner.pt"
    torch.save(winner.state_dict(), weights)
    report = OUT / "conclusion.txt"
    report.write_text(
        "Чесне порівняння: той самий seed, split, епохи й lr.\n"
        f"Найменший test MAE: {winner_name}.\n"
        f"Ваги: {weights.name}. Крива: {png.name}.\n",
        encoding="utf-8",
    )
    print("saved", png.name, weights.name, report.name)


if __name__ == "__main__":
    main()
