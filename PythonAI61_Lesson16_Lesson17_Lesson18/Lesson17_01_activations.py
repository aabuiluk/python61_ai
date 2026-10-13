"""Пара 17 · легко: чотири активації як шари."""

from torch import nn

for name, act in {
    "ReLU": nn.ReLU(),
    "Tanh": nn.Tanh(),
    "LeakyReLU": nn.LeakyReLU(),
    "Swish": nn.SiLU(),
}.items():
    print(name, act)
