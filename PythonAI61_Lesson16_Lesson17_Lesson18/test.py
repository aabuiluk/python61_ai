# import torch
# from torch import nn
#
# class RiskNet(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.lin = nn.Linear(1, 1)
#
#     def forward(self, x):
#         return self.lin(x)
#
# torch.manual_seed(0)
# model = RiskNet()
# x = torch.randn(4, 1)
# print(tuple(model(x).shape), len(list(model.parameters())))
# # -> (4, 1) 2   # вага і зсув

# import torch
# from torch import nn
#
# torch.manual_seed(0)
# x = torch.randn(32, 1)
# y = 0.5 * x
# model = nn.Linear(1, 1)
# opt = torch.optim.SGD(model.parameters(), lr=0.05)
# for epoch in range(15):
#     opt.zero_grad()
#     loss = ((model(x) - y) ** 2).mean()
#     loss.backward()
#     opt.step()
#     print(epoch, round(loss.item(), 4))
# # -> loss зменшується що епохиʼ

# import torch
# from torch import nn
#
# torch.manual_seed(42)
# x = torch.randn(100, 1)
# y = 0.7 * x + 0.2
# model = nn.Linear(1, 1)
# opt = torch.optim.SGD(model.parameters(), lr=0.01)
# history = []
# for _ in range(20):
#     opt.zero_grad()
#     loss = ((model(x) - y) ** 2).mean()
#     loss.backward()
#     opt.step()
#     history.append(loss.item())
# print(len(history), min(history) < history[0])
# print(history)
# # -> 20 True
#
# import torch
# from torch import nn
#
# model = nn.Linear(1, 1)
# print(list(model.state_dict().keys()))
# print(list(model.state_dict()))
# # -> ['weight', 'bias']

import torch
from torch import nn
import matplotlib.pyplot as plt

torch.manual_seed(42)
x = torch.randn(100, 1)
y = 0.7 * x + 0.2 + 0.1 * torch.randn_like(x)
model = nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.001)
hist = []
for _ in range(20):
    opt.zero_grad()
    loss = torch.nn.functional.mse_loss(model(x), y)
    loss.backward()
    opt.step()
    hist.append(loss.item())
with torch.no_grad():
    pred = model(x)

fig, axes = plt.subplots(1, 2, figsize=(9, 4))
axes[0].plot(range(1, 21), hist, marker="o", color="C0")
axes[0].set_xlabel("епоха")
axes[0].set_ylabel("MSE")
axes[0].set_title("Крива loss")
axes[1].scatter(y.numpy(), pred.numpy(), s=18, alpha=0.75, color="C0")
lo = min(float(y.min()), float(pred.min()))
hi = max(float(y.max()), float(pred.max()))
axes[1].plot([lo, hi], [lo, hi], color="0.4", linewidth=1)
axes[1].set_xlabel("y")
axes[1].set_ylabel("прогноз")
axes[1].set_title("Істина vs прогноз")
fig.tight_layout()
print(round(hist[0], 4), round(hist[-1], 4))
plt.show()
# # -> крива пада точки біля діагоналі