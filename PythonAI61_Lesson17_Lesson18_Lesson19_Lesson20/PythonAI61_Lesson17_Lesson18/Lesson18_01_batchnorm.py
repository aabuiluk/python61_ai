"""Пара 18 · легко: Sequential з BatchNorm1d."""

from torch import nn

print(nn.Sequential(nn.Linear(10, 32), nn.BatchNorm1d(32), nn.ReLU()))
