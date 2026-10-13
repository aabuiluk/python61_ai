"""Пара 19 · завдання 4. clip vs NaN при lr=1.0."""

import torch
from torch import nn

x = torch.randn(32, 16)
y = torch.randn(32, 1)


def run(clip: bool):
    layers: list[nn.Module] = [nn.Linear(16, 16), nn.ReLU()] * 6 + [nn.Linear(16, 1)]
    model = nn.Sequential(*layers)
    opt = torch.optim.SGD(model.parameters(), lr=1.0)
    last = None
    for _ in range(15):
        opt.zero_grad()
        loss = nn.functional.mse_loss(model(x), y)
        if not torch.isfinite(loss):
            return "NaN"
        loss.backward()
        if clip:
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        last = float(loss)
    return last

print("no clip", run(False), "clip", run(True))
