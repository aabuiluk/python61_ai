"""Пара 17 · середнє: різниця train/eval з Dropout."""

import torch
from torch import nn

layer = nn.Dropout(0.5)
x = torch.ones(4, 8)
layer.train()
print("train", layer(x).mean().item())
layer.eval()
print("eval", layer(x).mean().item())
