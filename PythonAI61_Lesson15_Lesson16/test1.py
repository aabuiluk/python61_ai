import torch

torch.manual_seed(42)
age = torch.tensor([34.0, 51.0, 28.0])
bmi = torch.randn(3, 2)
cube = torch.randn(2, 2, 2, requires_grad=True)
risk = age.mean() * bmi.mean() + cube.mean()
print(tuple(age.shape), tuple(bmi.shape), tuple(cube.shape), cube.requires_grad, risk.grad_fn is not None)
# -> (3,) (3, 2) (2, 2, 2) True True