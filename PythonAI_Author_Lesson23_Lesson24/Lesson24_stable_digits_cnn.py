"""Пара 24 · baseline vs BN+Dropout+clip на тих самих digits npz."""

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


class BaselineCNN(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv = nn.Conv2d(1, 16, 3)
        self.fc = nn.Linear(16 * 13 * 13, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = torch.relu(self.conv(x))
        h = torch.max_pool2d(h, 2)
        return self.fc(h.flatten(1))


class StableCNN(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv = nn.Conv2d(1, 16, 3)
        self.bn = nn.BatchNorm2d(16)
        self.drop = nn.Dropout(0.3)
        self.fc = nn.Linear(16 * 13 * 13, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.drop(torch.relu(self.bn(self.conv(x))))
        h = torch.max_pool2d(h, 2)
        return self.fc(h.flatten(1))


def run(model: nn.Module, loader, x_te, y_te, epochs: int = 4, clip: bool = False) -> float:
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()
    for _ in range(epochs):
        model.train()
        for xb, yb in loader:
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            if clip:
                nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
    model.eval()
    with torch.no_grad():
        return float((model(x_te).argmax(1) == y_te).float().mean())


def main() -> None:
    torch.manual_seed(44)
    x_tr, y_tr = load_split("digits_train.npz")
    x_te, y_te = load_split("digits_test.npz")
    mean, std = float(x_tr.mean()), float(x_tr.std())
    x_tr = (x_tr - mean) / (std + 1e-6)
    x_te = (x_te - mean) / (std + 1e-6)
    loader = DataLoader(TensorDataset(x_tr, y_tr), batch_size=64, shuffle=True)

    # clip demo on fixed grad vector
    g = torch.tensor([3.0, 4.0])
    norm = float(torch.linalg.vector_norm(g))
    clipped = g * (1.0 / norm)
    print("clip demo", [round(float(v), 3) for v in clipped], "from norm", round(norm, 3))

    base_acc = run(BaselineCNN(), loader, x_te, y_te, clip=False)
    stable_acc = run(StableCNN(), loader, x_te, y_te, clip=True)
    print("baseline_acc", round(base_acc, 3))
    print("stable_BN_Dropout_clip_acc", round(stable_acc, 3))
    print("delta", round(stable_acc - base_acc, 3), "(може бути близько нуля на короткому бюджеті)")


if __name__ == "__main__":
    main()
