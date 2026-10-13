"""Спільний код пари 25: дані рентгенів, мала CNN для пневмонії, метрики.

Дані — PneumoniaMNIST 64×64 (MedMNIST v2, CC BY 4.0), похідний від Kaggle Chest X-Ray Pneumonia.
Клас 0 = NORMAL, клас 1 = PNEUMONIA.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torch import nn

HERE = Path(__file__).resolve().parent
XRAY = HERE / "assets" / "xray"
MODELS = HERE / "models"
CLASSES = ("NORMAL", "PNEUMONIA")


def load_split(split: str) -> tuple[torch.Tensor, torch.Tensor]:
    """split = train | val | test → (N,1,64,64) у [0,1] і мітки (N,)."""
    blob = np.load(XRAY / "pneumoniamnist_64.npz")
    images = torch.from_numpy(blob[f"{split}_images"]).float().unsqueeze(1) / 255.0
    labels = torch.from_numpy(blob[f"{split}_labels"].ravel().astype(np.int64))
    return images, labels


class PneumoniaCNN(nn.Module):
    """Три блоки Conv→BatchNorm→ReLU→MaxPool, далі GlobalAvgPool і Linear(64, 2)."""

    def __init__(self) -> None:
        super().__init__()

        def block(c_in: int, c_out: int) -> nn.Sequential:
            return nn.Sequential(
                nn.Conv2d(c_in, c_out, 3, padding=1),
                nn.BatchNorm2d(c_out),
                nn.ReLU(),
                nn.MaxPool2d(2),
            )

        self.features = nn.Sequential(block(1, 16), block(16, 32), block(32, 64))  # 64→32→16→8
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.head = nn.Sequential(nn.Dropout(0.3), nn.Linear(64, 2))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.head(self.pool(self.features(x)).flatten(1))


def load_checkpoint(path: Path) -> tuple[PneumoniaCNN, float, float]:
    blob = torch.load(path, map_location="cpu")
    model = PneumoniaCNN()
    model.load_state_dict(blob["model_state"])
    model.eval()
    return model, float(blob["mean"]), float(blob["std"])


def png_to_tensor(path: Path, mean: float, std: float) -> torch.Tensor:
    """Будь-який PNG/JPG рентгена → (1,1,64,64), нормалізований як train."""
    img = Image.open(path).convert("L").resize((64, 64), Image.BILINEAR)
    x = torch.from_numpy(np.array(img, dtype=np.float32) / 255.0).view(1, 1, 64, 64)
    return (x - mean) / (std + 1e-6)


def binary_metrics(y_true: torch.Tensor, y_pred: torch.Tensor) -> dict[str, float]:
    """Accuracy, Precision, Recall, F1 для класу PNEUMONIA (=1) і confusion matrix."""
    tp = int(((y_pred == 1) & (y_true == 1)).sum())
    tn = int(((y_pred == 0) & (y_true == 0)).sum())
    fp = int(((y_pred == 1) & (y_true == 0)).sum())
    fn = int(((y_pred == 0) & (y_true == 1)).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "accuracy": (tp + tn) / max(1, len(y_true)),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
    }


def print_metrics(m: dict[str, float]) -> None:
    print(f"accuracy  {m['accuracy']:.3f}")
    print(f"precision {m['precision']:.3f}   (з тих, кого назвали PNEUMONIA, скільки справді хворі)")
    print(f"recall    {m['recall']:.3f}   (скільки хворих модель знайшла)")
    print(f"f1        {m['f1']:.3f}")
    print("confusion matrix (рядки = правда, стовпці = прогноз)")
    print(f"              NORMAL  PNEUMONIA")
    print(f"NORMAL     {m['tn']:>8} {m['fp']:>10}")
    print(f"PNEUMONIA  {m['fn']:>8} {m['tp']:>10}")
