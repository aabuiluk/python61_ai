"""Пара 23 · перевірка PNG digit_{0-9}_v{1-3}.png після навчання."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torch import nn

ROOT = Path(__file__).resolve().parent / "assets" / "digits"
CKPT = Path("mnist_cnn.pth")


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


def main() -> None:
    if not CKPT.is_file():
        raise SystemExit("Спочатку запустіть Lesson23_train_digits_cnn.py")
    blob = torch.load(CKPT, map_location="cpu")
    model = DigitsCNN()
    model.load_state_dict(blob["model_state"])
    model.eval()
    mean = float(blob["mean"])
    std = float(blob["std"])
    png_dir = ROOT / "png"
    ok = 0
    total = 0
    for digit in range(10):
        for ver in (1, 2, 3):
            path = png_dir / f"digit_{digit}_v{ver}.png"
            arr = np.array(Image.open(path).convert("L").resize((28, 28)))
            x = torch.from_numpy(arr).float().view(1, 1, 28, 28) / 255.0
            x = (x - mean) / (std + 1e-6)
            with torch.no_grad():
                guess = int(model(x).argmax(1).item())
            total += 1
            ok += int(guess == digit)
            print(f"{path.name} -> {guess} (ожидали {digit})")
    print("png_match", ok, "/", total)


if __name__ == "__main__":
    main()
