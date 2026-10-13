"""Пара 25 · LeNet, AlexNet, ResNet на одному батчі CIFAR-форми (4, 3, 32, 32).

Друкує форму виходу і кількість параметрів кожної мережі, а потім показує,
що робить залишкове зʼєднання (skip connection) у блоці ResNet,
і чим LayerNorm відрізняється від BatchNorm.
"""

from __future__ import annotations

import torch
from torch import nn


class LeNet5(nn.Module):
    """LeCun, 1998: дві згортки 5×5 + три повнозвʼязні шари."""

    def __init__(self, n_classes: int = 10) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 6, 5), nn.ReLU(), nn.MaxPool2d(2),   # 32 → 28 → 14
            nn.Conv2d(6, 16, 5), nn.ReLU(), nn.MaxPool2d(2),  # 14 → 10 → 5
        )
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(16 * 5 * 5, 120), nn.ReLU(),
            nn.Linear(120, 84), nn.ReLU(),
            nn.Linear(84, n_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.head(self.features(x))


class MiniAlexNet(nn.Module):
    """Ідея AlexNet (2012) у масштабі 32×32: більше каналів, ReLU, Dropout у голові."""

    def __init__(self, n_classes: int = 10) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),     # 32 → 16
            nn.Conv2d(64, 192, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),   # 16 → 8
            nn.Conv2d(192, 384, 3, padding=1), nn.ReLU(),
            nn.Conv2d(384, 256, 3, padding=1), nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),  # 8 → 4
        )
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.5), nn.Linear(256 * 4 * 4, 1024), nn.ReLU(),
            nn.Dropout(0.5), nn.Linear(1024, n_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.head(self.features(x))


class ResidualBlock(nn.Module):
    """y = ReLU(F(x) + x): градієнт має «обхідну дорогу» через + x."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.body = nn.Sequential(
            nn.Conv2d(channels, channels, 3, padding=1, bias=False),
            nn.BatchNorm2d(channels),
            nn.ReLU(),
            nn.Conv2d(channels, channels, 3, padding=1, bias=False),
            nn.BatchNorm2d(channels),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.relu(self.body(x) + x)


def count_params(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters())


def main() -> None:
    torch.manual_seed(25)
    batch = torch.randn(4, 3, 32, 32)  # форма батча CIFAR-10: 4 картинки, RGB, 32×32

    models: dict[str, nn.Module] = {"LeNet-5": LeNet5(), "MiniAlexNet": MiniAlexNet()}
    try:
        from torchvision.models import resnet18

        models["ResNet-18"] = resnet18(weights=None, num_classes=10)
    except ImportError:
        print("torchvision не встановлено — ResNet-18 пропускаємо (pip install torchvision)")

    print(f"{'мережа':<14}{'вихід':<18}{'параметрів':>14}")
    for name, model in models.items():
        model.eval()
        with torch.no_grad():
            out = model(batch)
        print(f"{name:<14}{str(tuple(out.shape)):<18}{count_params(model):>14,}")

    print("\nЗалишковий блок: вихід тієї ж форми, що й вхід")
    block = ResidualBlock(16).eval()
    x = torch.randn(2, 16, 8, 8)
    with torch.no_grad():
        y = block(x)
    print("x", tuple(x.shape), "→ y", tuple(y.shape))

    # Якщо всі ваги тіла нульові, блок пропускає вхід (після ReLU) без змін — «тотожність за замовчуванням».
    for p in block.body.parameters():
        nn.init.zeros_(p)
    with torch.no_grad():
        same = torch.allclose(block(x), torch.relu(x))
    print("нульове тіло → вихід = ReLU(x):", same)

    print("\nBatchNorm vs LayerNorm на тензорі (2, 4, 3, 3)")
    t = torch.randn(2, 4, 3, 3) * 5 + 3
    with torch.no_grad():
        bn = nn.BatchNorm2d(4).train()(t)
        ln = nn.LayerNorm([4, 3, 3])(t)
    print("до нормалізації: середнє", round(float(t.mean()), 2), "std", round(float(t.std()), 2))
    print("BatchNorm2d: середнє по (batch, H, W) для каналу 0 =", abs(round(float(bn[:, 0].mean()), 4)))
    print("LayerNorm:   середнє по (C, H, W) для прикладу 0   =", abs(round(float(ln[0].mean()), 4)))
    # -> обидва ≈ 0, але BatchNorm рахує статистику по батчу, а LayerNorm — всередині одного прикладу


if __name__ == "__main__":
    main()
