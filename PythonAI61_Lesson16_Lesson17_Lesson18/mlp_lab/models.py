"""MLP як nn.Module: шари в __init__, рахунок у forward.

Порядок прихованого блоку на цій лабораторії:
Linear → (BatchNorm) → ReLU → (Dropout).
"""

from __future__ import annotations

from torch import nn

from data import DROPOUT_P, HIDDEN, N_FEATURES


class MLP(nn.Module):
    def __init__(
        self,
        *,
        in_features: int = N_FEATURES,
        hidden: int = HIDDEN,
        use_bn: bool = False,
        dropout_p: float = 0.0,
    ) -> None:
        super().__init__()
        layers: list[nn.Module] = [nn.Linear(in_features, hidden)]
        if use_bn:
            layers.append(nn.BatchNorm1d(hidden))
        layers.append(nn.ReLU())
        if dropout_p > 0:
            layers.append(nn.Dropout(dropout_p))
        layers.append(nn.Linear(hidden, 1))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)


CONFIGS: tuple[tuple[str, bool, float], ...] = (
    ("MLP", False, 0.0),
    ("MLP+Dropout", False, DROPOUT_P),
    ("MLP+BatchNorm", True, 0.0),
    ("MLP+Dropout+BN", True, DROPOUT_P),
)
