"""Тестові метрики лише в eval() і під torch.no_grad()."""

from __future__ import annotations

import torch
from sklearn.metrics import mean_absolute_error, r2_score
from torch import nn

from data import Tensors


def test_metrics(model: nn.Module, data: Tensors) -> tuple[float, float, float]:
    model.eval()
    with torch.no_grad():
        pred_te = model(data.x_test).numpy().ravel()
        pred_tr = model(data.x_train).numpy().ravel()
    mae = float(mean_absolute_error(data.y_test, pred_te))
    r2 = float(r2_score(data.y_test, pred_te))
    mae_tr = float(mean_absolute_error(data.y_train.numpy().ravel(), pred_tr))
    gap = mae_tr - mae
    return mae, r2, gap
