"""Пара 15 · складніше: Sequential MLP і лічильник параметрів."""

from torch import nn

mlp = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 1))
n_params = sum(p.numel() for p in mlp.parameters())
print("params", n_params)
print(mlp)
# -> params 33  (2*8+8 + 8*1+1)
