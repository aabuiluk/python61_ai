"""Пара 15 · завдання 1. Тензори HealthRisk."""

import torch

torch.manual_seed(42)
vec = torch.linspace(20, 70, 5)
mat = torch.randn(4, 3)
cube = torch.randn(2, 2, 2, requires_grad=True)
risk = vec.mean() + mat.mean() * cube.mean()
print(tuple(vec.shape), tuple(mat.shape), tuple(cube.shape), cube.requires_grad)
print("risk", float(risk.detach()), "has_grad_fn", risk.grad_fn is not None)
