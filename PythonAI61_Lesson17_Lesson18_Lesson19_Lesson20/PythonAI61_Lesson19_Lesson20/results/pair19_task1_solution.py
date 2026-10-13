"""Пара 19 · завдання 1. σ і σ'."""

import torch
x = torch.linspace(-6, 6, 13)
s = torch.sigmoid(x)
print("x sigma sigma'")
for a, b, c in zip(x, s, s * (1 - s)):
    print(f"{float(a):6.1f} {float(b):8.4f} {float(c):8.4f}")
