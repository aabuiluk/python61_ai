"""Пара 16 · середнє: мінімальний nn.Module."""

import torch
from torch import nn

class Tiny(nn.Module):
    def __init__(self):
        super().__init__()
        self.lin = nn.Linear(1, 1)

    def forward(self, x):
        return self.lin(x)

print(tuple(Tiny()(torch.randn(4, 1)).shape))
# -> (4, 1)
