"""Пара 25 · transfer learning: ResNet18 (ImageNet) із замороженими згортками + Linear(512, 2).

Сценарій домашнього завдання 5.2 на локальних даних:
    resize 224×224 і нормалізація ImageNet → ResNet18 з замороженими шарами →
    новий класифікатор Linear(512, 2) → CrossEntropyLoss, Adam(lr=1e-4), 5 епох →
    Accuracy / Precision / Recall / F1, confusion matrix →
    pneumonia_resnet18.pth і pneumonia_predictions.png (8 випадкових знімків з test).

Перший запуск завантажує ваги ImageNet (~45 МБ) у кеш torch, далі працює офлайн.
Згортки заморожені, тому ознаки 512 рахуємо ОДИН раз для всіх знімків, а вчимо лише Linear:
це той самий результат, що й прогін повної мережі щоепохи, але в рази швидше на CPU.

    python Lesson25_03_resnet18_transfer.py
    python Lesson25_03_resnet18_transfer.py --limit 600     # швидка перевірка на частині даних
"""

from __future__ import annotations

import argparse
import random
import ssl
from pathlib import Path

import torch
from PIL import Image, ImageDraw
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from pneumonia_model import CLASSES, binary_metrics, load_split, print_metrics

IMAGENET_MEAN = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
IMAGENET_STD = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)


def use_certifi() -> None:
    """Python з python.org на macOS часто не бачить системних сертифікатів — беремо їх з certifi."""
    try:
        import certifi
    except ImportError:
        return
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())


def load_imagenet_resnet18():
    from torchvision.models import ResNet18_Weights, resnet18

    use_certifi()
    try:
        return resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
    except Exception as exc:  # мережа, проксі, сертифікати
        raise SystemExit(
            f"Не вдалося завантажити ваги ImageNet: {exc}\n"
            "Перевірте інтернет. На macOS: python -m pip install certifi "
            "або запустіть «Install Certificates.command» з папки Python."
        )


def to_resnet_input(x: torch.Tensor) -> torch.Tensor:
    """(N,1,64,64) у [0,1] → (N,3,224,224) з нормалізацією ImageNet."""
    x = nn.functional.interpolate(x, size=(224, 224), mode="bilinear", align_corners=False)
    return (x.repeat(1, 3, 1, 1) - IMAGENET_MEAN) / IMAGENET_STD


def extract_features(backbone: nn.Module, x: torch.Tensor, name: str) -> torch.Tensor:
    feats = []
    with torch.no_grad():
        for i, chunk in enumerate(x.split(64)):
            feats.append(backbone(to_resnet_input(chunk)))
            print(f"\r  ознаки {name}: {min((i + 1) * 64, len(x))}/{len(x)}", end="", flush=True)
    print()
    return torch.cat(feats)


def save_predictions_png(images, labels, preds, path: Path) -> None:
    pick = random.Random(25).sample(range(len(labels)), 8)
    tile, pad = 192, 34
    sheet = Image.new("RGB", (4 * tile, 2 * (tile + pad)), "white")
    draw = ImageDraw.Draw(sheet)
    for n, i in enumerate(pick):
        img = Image.fromarray((images[i, 0].numpy() * 255).astype("uint8")).resize((tile, tile))
        x0, y0 = (n % 4) * tile, (n // 4) * (tile + pad)
        sheet.paste(img.convert("RGB"), (x0, y0))
        ok = int(preds[i]) == int(labels[i])
        draw.text(
            (x0 + 6, y0 + tile + 4),
            f"pred {CLASSES[int(preds[i])]}\ntrue {CLASSES[int(labels[i])]}",
            fill=(0, 120, 0) if ok else (200, 0, 0),
        )
    sheet.save(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--limit", type=int, default=0, help="взяти лише перші N знімків кожного спліту")
    args = parser.parse_args()

    try:
        import torchvision  # noqa: F401
    except ImportError:
        raise SystemExit("Потрібен torchvision: python -m pip install torchvision")

    torch.manual_seed(25)
    splits = {name: load_split(name) for name in ("train", "val", "test")}
    if args.limit:
        splits = {k: (x[: args.limit], y[: args.limit]) for k, (x, y) in splits.items()}

    model = load_imagenet_resnet18()
    for p in model.parameters():
        p.requires_grad = False  # заморожуємо всі згорткові шари
    model.fc = nn.Linear(512, 2)  # новий класифікатор — єдине, що вчимо
    backbone = nn.Sequential(*list(model.children())[:-1], nn.Flatten()).eval()

    feats = {k: extract_features(backbone, x, k) for k, (x, _) in splits.items()}
    y_tr = splits["train"][1]
    counts = torch.bincount(y_tr, minlength=2).float()
    loss_fn = nn.CrossEntropyLoss(weight=counts.sum() / (2 * counts))
    opt = torch.optim.Adam(model.fc.parameters(), lr=args.lr)
    loader = DataLoader(TensorDataset(feats["train"], y_tr), batch_size=32, shuffle=True)

    for epoch in range(1, args.epochs + 1):
        model.fc.train()
        total = 0.0
        for fb, yb in loader:
            opt.zero_grad()
            loss = loss_fn(model.fc(fb), yb)
            loss.backward()
            opt.step()
            total += float(loss.item()) * len(yb)
        with torch.no_grad():
            val = binary_metrics(splits["val"][1], model.fc(feats["val"]).argmax(1))
        print(f"epoch {epoch}  loss {total / len(y_tr):.4f}  val_acc {val['accuracy']:.3f}  val_f1 {val['f1']:.3f}")

    with torch.no_grad():
        preds = model.fc(feats["test"]).argmax(1)
    print("\nTEST")
    print_metrics(binary_metrics(splits["test"][1], preds))

    torch.save(model.state_dict(), "pneumonia_resnet18.pth")
    save_predictions_png(splits["test"][0], splits["test"][1], preds, Path("pneumonia_predictions.png"))
    print("\nзбережено pneumonia_resnet18.pth і pneumonia_predictions.png")


if __name__ == "__main__":
    main()
