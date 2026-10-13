"""Спільні дані лабораторії пар 16–18.

Seed, split, scaler і кількість епох фіксовані: інакше чотири конфіги
неможливо чесно порівняти.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

SEED = 42
N_SAMPLES = 2000
N_FEATURES = 10
TEST_SIZE = 0.2
EPOCHS = 40
LR = 1e-3
HIDDEN = 32
DROPOUT_P = 0.3


@dataclass(frozen=True)
class Tensors:
    x_train: torch.Tensor
    y_train: torch.Tensor
    x_test: torch.Tensor
    y_test: np.ndarray


def set_seeds(seed: int = SEED) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)


def load_tensors(seed: int = SEED) -> Tensors:
    set_seeds(seed)
    x, y = make_regression(
        n_samples=N_SAMPLES,
        n_features=N_FEATURES,
        noise=10.0,
        random_state=seed,
    )
    x_tr, x_te, y_tr, y_te = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=seed
    )
    scaler = StandardScaler().fit(x_tr)
    return Tensors(
        x_train=torch.tensor(scaler.transform(x_tr), dtype=torch.float32),
        y_train=torch.tensor(y_tr, dtype=torch.float32).view(-1, 1),
        x_test=torch.tensor(scaler.transform(x_te), dtype=torch.float32),
        y_test=y_te,
    )
