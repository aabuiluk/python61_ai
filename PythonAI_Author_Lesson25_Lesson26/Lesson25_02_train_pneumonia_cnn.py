"""Пара 25 · навчання малої CNN на рентгенах грудної клітки (NORMAL / PNEUMONIA).

Дані: assets/xray/pneumoniamnist_64.npz — train 4708, val 524, test 624 знімків 64×64.
У train хворих утричі більше, ніж здорових, тому loss зважуємо за класами.
Аугментація (яскравість, масштаб, зсув, розмиття) робить модель стійкою до чужих знімків:
без неї мережа запамʼятовує дрібну текстуру і ламається після звичайного resize.
Найкращу епоху вибираємо за balanced accuracy на val, а test дивимось один раз у кінці.

    python Lesson25_02_train_pneumonia_cnn.py                 # → pneumonia_cnn.pth у поточній папці
    python Lesson25_02_train_pneumonia_cnn.py --epochs 4      # швидкий прогін
    python Lesson25_02_train_pneumonia_cnn.py --no-aug        # порівняти без аугментації
"""

from __future__ import annotations

import argparse
import copy
from pathlib import Path

import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, TensorDataset

from pneumonia_model import PneumoniaCNN, binary_metrics, load_split, print_metrics


def augment(xb: torch.Tensor) -> torch.Tensor:
    """Батч (N,1,64,64) у [0,1] → ті самі знімки, трохи змінені випадковим чином."""
    n = len(xb)
    contrast = torch.empty(n, 1, 1, 1).uniform_(0.8, 1.2)
    brightness = torch.empty(n, 1, 1, 1).uniform_(-0.1, 0.1)
    mean = xb.mean((2, 3), keepdim=True)
    xb = ((xb - mean) * contrast + mean + brightness).clamp(0, 1)

    scale = torch.empty(n).uniform_(0.85, 1.05)  # наближення / віддалення
    theta = torch.zeros(n, 2, 3)
    theta[:, 0, 0] = scale
    theta[:, 1, 1] = scale
    theta[:, :, 2] = torch.empty(n, 2).uniform_(-0.08, 0.08)  # зсув до ~3 px
    grid = F.affine_grid(theta, list(xb.shape), align_corners=False)
    xb = F.grid_sample(xb, grid, padding_mode="border", align_corners=False)

    if torch.rand(1).item() < 0.5:  # розмиття, як після чужого resize
        if torch.rand(1).item() < 0.5:
            xb = F.avg_pool2d(xb, 3, stride=1, padding=1, count_include_pad=False)
        else:
            xb = F.interpolate(F.interpolate(xb, scale_factor=0.5, mode="bilinear"), size=64, mode="bilinear")
    return xb


def predict(model: nn.Module, x: torch.Tensor) -> torch.Tensor:
    model.eval()
    with torch.no_grad():
        return torch.cat([model(chunk).argmax(1) for chunk in x.split(256)])


def balanced_accuracy(y: torch.Tensor, pred: torch.Tensor) -> float:
    """Середнє з точності на здорових і точності на хворих — не дає «виграти», кажучи всім PNEUMONIA."""
    return 0.5 * (float((pred[y == 0] == 0).float().mean()) + float((pred[y == 1] == 1).float().mean()))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--no-aug", action="store_true")
    parser.add_argument("--out", default="pneumonia_cnn.pth")
    args = parser.parse_args()

    torch.manual_seed(25)
    x_tr, y_tr = load_split("train")
    x_va, y_va = load_split("val")
    x_te, y_te = load_split("test")
    mean, std = float(x_tr.mean()), float(x_tr.std())  # статистика лише з train

    def norm(x: torch.Tensor) -> torch.Tensor:
        return (x - mean) / (std + 1e-6)

    counts = torch.bincount(y_tr, minlength=2).float()
    weights = counts.sum() / (2 * counts)  # рідший клас (NORMAL) важить більше
    print("train:", {"NORMAL": int(counts[0]), "PNEUMONIA": int(counts[1])}, "ваги loss:", weights.tolist())

    model = PneumoniaCNN()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss(weight=weights)
    loader = DataLoader(TensorDataset(x_tr, y_tr), batch_size=64, shuffle=True)

    best_score, best_state, history = -1.0, None, []
    for epoch in range(1, args.epochs + 1):
        model.train()
        total = 0.0
        for xb, yb in loader:
            if not args.no_aug:
                xb = augment(xb)
            opt.zero_grad()
            loss = loss_fn(model(norm(xb)), yb)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # обрізання градієнтів
            opt.step()
            total += float(loss.item()) * len(yb)
        val_pred = predict(model, norm(x_va))
        score = balanced_accuracy(y_va, val_pred)
        history.append({"loss": total / len(y_tr), "val_balanced_acc": score})
        print(f"epoch {epoch:>2}  loss {total / len(y_tr):.4f}  val_balanced_acc {score:.3f}")
        if score > best_score:
            best_score, best_state = score, copy.deepcopy(model.state_dict())

    model.load_state_dict(best_state)
    test_pred = predict(model, norm(x_te))
    test = binary_metrics(y_te, test_pred)
    test["balanced_accuracy"] = balanced_accuracy(y_te, test_pred)
    print(f"\nTEST (один раз, найкраща епоха за val: {best_score:.3f})")
    print_metrics(test)
    print(f"balanced  {test['balanced_accuracy']:.3f}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state": model.state_dict(),
            "mean": mean,
            "std": std,
            "classes": ["NORMAL", "PNEUMONIA"],
            "history": history,
            "test_metrics": test,
            "data": "PneumoniaMNIST 64x64 (MedMNIST v2, CC BY 4.0)",
        },
        out,
    )
    print("\nзбережено", out.resolve())


if __name__ == "__main__":
    main()
