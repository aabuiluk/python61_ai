"""Пара 20 · складніше: голова бінарної класифікації."""

from torch import nn
print(nn.Sequential(nn.Linear(30, 16), nn.ReLU(), nn.Linear(16, 1)))
print("loss = BCEWithLogitsLoss")
