"""Пара 15 · легко: тензори 1D/2D і requires_grad."""

import torch

torch.manual_seed(42)
age = torch.tensor([21.0, 34.0, 45.0])
bmi = torch.randn(3, 1, requires_grad=True)
print("age", tuple(age.shape), "bmi", tuple(bmi.shape), "grad", bmi.requires_grad)
print((age.unsqueeze(1) * bmi).mean().item())
# -> age (3,) bmi (3, 1) grad True
# -> число (залежить від seed 42)
