"""Пара 26 · навчання CharCNN: 36 класів (A–Z, 0–9), символи 28×28.

Дані: assets/chars/chars_train.npz і chars_test.npz (images, labels, alphabet).
Символи надруковані різними шрифтами, з поворотом, товщиною і шумом.

    python Lesson26_01_train_char_cnn.py                # → ocr_char_cnn.pth у поточній папці
    python Lesson26_01_train_char_cnn.py --epochs 2     # швидкий прогін
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from ocr_model import CHARS, CharCNN


def load(name: str):
    blob = np.load(CHARS / name)
    x = torch.from_numpy(blob["images"]).float().unsqueeze(1) / 255.0
    y = torch.from_numpy(blob["labels"].astype(np.int64))
    return x, y, str(blob["alphabet"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=6)
    parser.add_argument("--out", default="ocr_char_cnn.pth")
    args = parser.parse_args()

    torch.manual_seed(26)
    x_tr, y_tr, alphabet = load("chars_train.npz")
    x_te, y_te, _ = load("chars_test.npz")
    print("train", tuple(x_tr.shape), "test", tuple(x_te.shape), "класів", len(alphabet))

    model = CharCNN(len(alphabet))
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()
    loader = DataLoader(TensorDataset(x_tr, y_tr), batch_size=128, shuffle=True)
    for epoch in range(1, args.epochs + 1):
        model.train()
        total = 0.0
        for xb, yb in loader:
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
            total += float(loss.item()) * len(yb)
        model.eval()
        with torch.no_grad():
            pred = model(x_te).argmax(1)
        acc = float((pred == y_te).float().mean())
        print(f"epoch {epoch}  loss {total / len(y_tr):.4f}  test_acc {acc:.3f}")

    confusions: dict[tuple[str, str], int] = {}
    for t, p in zip(y_te.tolist(), pred.tolist()):
        if t != p:
            key = (alphabet[t], alphabet[p])
            confusions[key] = confusions.get(key, 0) + 1
    top = sorted(confusions.items(), key=lambda kv: -kv[1])[:8]
    print("найчастіші плутанини (правда → прогноз):", ", ".join(f"{a}→{b}×{n}" for (a, b), n in top))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model_state": model.state_dict(), "alphabet": alphabet, "test_acc": acc}, out)
    print("збережено", out.resolve())


if __name__ == "__main__":
    main()
