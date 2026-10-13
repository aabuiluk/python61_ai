import torch

xb = torch.randn(8, 1, 28, 28)
yb = torch.randint(0, 10, (8,), dtype=torch.long)
print(tuple(xb.shape), tuple(yb.shape), yb.dtype)
# -> (8, 1, 28, 28) (8,) torch.int64