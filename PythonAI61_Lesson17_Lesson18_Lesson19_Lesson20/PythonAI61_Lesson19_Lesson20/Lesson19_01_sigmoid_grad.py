"""Пара 19 · легко: сітка сигмоїди та похідної."""

import torch
x = torch.linspace(-4, 4, 9)
s = torch.sigmoid(x)
print(torch.stack([x, s, s * (1 - s)], 1))
