"""Пара 21 · форма сірого і кольорового кадру."""

import torch

gray = torch.zeros(1, 1, 28, 28)
rgb = torch.zeros(4, 3, 32, 32)
print("gray", tuple(gray.shape), gray.numel())
print("rgb", tuple(rgb.shape), rgb.numel())
