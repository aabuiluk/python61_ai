"""Пара 23 · повне навчання CNN на локальних digits_*.npz."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

ROOT = Path(__file__).resolve().parent / "assets" / "digits"


def load_split(name: str):
    blob = np.load(ROOT / name)
    images = torch.from_numpy(blob["images"]).float().unsqueeze(1) / 255.0
    labels = torch.from_numpy(blob["labels"]).long()
    return images, labels


def main() -> None:
    torch.manual_seed(44)
    x_tr, y_tr = load_split("digits_train.npz")
    x_te, y_te = load_split("digits_test.npz")
    mean, std = float(x_tr.mean()), float(x_tr.std())
    x_tr = (x_tr - mean) / (std + 1e-6)
    x_te = (x_te - mean) / (std + 1e-6)

    class DigitsCNN(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(1, 16, 3),
                nn.ReLU(),
                nn.MaxPool2d(2),
            )
            self.head = nn.Linear(16 * 13 * 13, 10)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.head(self.features(x).flatten(1))

    model = DigitsCNN()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()
    loader = DataLoader(TensorDataset(x_tr, y_tr), batch_size=64, shuffle=True)
    history: list[float] = []
    for epoch in range(5):
        model.train()
        total = 0.0
        for xb, yb in loader:
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
            total += float(loss.item()) * len(yb)
        history.append(total / len(y_tr))
        print(f"epoch {epoch + 1} loss {history[-1]:.4f}")

    model.eval()
    with torch.no_grad():
        acc = float((model(x_te).argmax(1) == y_te).float().mean())
    ckpt = {
        "model_state": model.state_dict(),
        "arch": "Conv2d(1,16,3)+MaxPool2d(2)+Linear(2704,10)",
        "history": history,
        "mean": mean,
        "std": std,
    }
    out = Path("mnist_cnn.pth")
    torch.save(ckpt, out)
    print("test_acc", round(acc, 3), "saved", out.resolve())


if __name__ == "__main__":
    main()
