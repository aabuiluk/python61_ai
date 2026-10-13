"""Один крок навчання: zero_grad → forward → loss → backward → step."""

from __future__ import annotations

import torch
from torch import nn

from data import EPOCHS, LR, Tensors


def train(
    model: nn.Module,
    data: Tensors,
    *,
    epochs: int = EPOCHS,
    lr: float = LR,
) -> list[float]:
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    history: list[float] = []
    for _ in range(epochs):
        model.train()
        opt.zero_grad()
        pred = model(data.x_train)
        loss = nn.functional.mse_loss(pred, data.y_train)
        loss.backward()
        opt.step()
        history.append(float(loss.item()))
    return history
