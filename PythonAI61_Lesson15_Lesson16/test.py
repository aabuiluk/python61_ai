# import torch
# from torch import nn
#
# torch.manual_seed(42)
# area = torch.tensor([[4.0], [6.0], [9.0],  [5.0]])  # 40, 60, 90 м²
# layer = nn.Linear(1, 1)
# price_hat = layer(area)
# print(layer.weight.item(), layer.bias.item(), tuple(price_hat.shape))
# # -> w і b випадкові, форма прогнозу (3, 1)

# import torch
#
# torch.manual_seed(42)
# bmi = torch.tensor([[22.0], [27.4], [31.1]])
# print("клієнтів", bmi.shape[0], "ознак", bmi.shape[1])
# # -> клієнтів 3 ознак 1

# import torch
# from torch import nn
#
# torch.manual_seed(42)
# x = torch.randn(8, 1)
# layer = nn.Linear(1, 1)
# y_hat = layer(x)
# print(round(layer.weight.item(), 4), round(layer.bias.item(), 4), tuple(y_hat.shape))
# # -> вага, зсув і форма (8, 1)

# w, x, y = 0.3, 2.0, 1.0
# pred = w * x
# err = pred - y
# loss = err ** 2
# grad_w = 2 * err * x
# print(pred, err, loss, grad_w)
# # -> 0.6 -0.4 0.16 -1.6

# import torch
#
# w = torch.tensor([0.3], requires_grad=True)
# x = torch.tensor([2.0])
# y = torch.tensor([1.0])
# loss = (w * x - y).pow(2).mean()
# loss.backward()
# print(loss.item(), float(w.grad))
# # -> 0.16 -1.6

# import torch
# from torch import nn
# import matplotlib.pyplot as plt
#
# torch.manual_seed(0)
# x = torch.linspace(-2, 2, 5).unsqueeze(1)
# plain = nn.Sequential(nn.Linear(1, 4), nn.Linear(4, 1))
# bent = nn.Sequential(nn.Linear(1, 4), nn.ReLU(), nn.Linear(4, 1))
# print(plain(x).detach().reshape(-1).tolist())
# print(bent(x).detach().reshape(-1).tolist())
#
# xs = torch.linspace(-2, 2, 200).unsqueeze(1)
# fig, ax = plt.subplots(figsize=(7, 4))
# ax.plot(xs, plain(xs).detach(), label="Linear → Linear")
# ax.plot(xs, bent(xs).detach(), label="Linear → ReLU → Linear")
# ax.set_xlabel("x")
# ax.set_ylabel("ŷ")
# ax.legend()
# ax.grid(True, alpha=0.3)
# plt.show()

from torch import nn

mlp = nn.Sequential(
    nn.Linear(8, 8),
    nn.ReLU(),
    nn.Linear(8, 4),
)
n_params = sum(p.numel() for p in mlp.parameters())
print(n_params)
# -> 33  (2*8+8 + 8*1+1)