# # import torch
# # from torch import nn
# #
# # torch.manual_seed(42)
# # x = torch.ones(2, 6)
# # layer = nn.Dropout(p=0.5)
# # layer.train()
# # train_out = layer(x)
# # layer.eval()
# # eval_out = layer(x)
# # print("x    ", x[0].tolist())
# # print("train", train_out[0].tolist(), "mean", round(float(train_out.mean()), 3))
# # print("eval ", eval_out[0].tolist(), "mean", round(float(eval_out.mean()), 3))
# # # -> train: нулі й двійки; eval: самі одиниці, mean=1.0
#
#
# import torch
# from torch import nn
# import matplotlib.pyplot as plt
#
# torch.manual_seed(42)
# x = torch.ones(2, 6)
# layer = nn.Dropout(p=0.5)
# layer.train()
# train_out = layer(x)
# layer.eval()
# eval_out = layer(x)
#
# idx = list(range(6))
# fig, ax = plt.subplots(figsize=(8, 4))
# ax.bar([i - 0.2 for i in idx], train_out[0].tolist(), 0.4, label="train()", color="C0")
# ax.bar([i + 0.2 for i in idx], eval_out[0].tolist(), 0.4, label="eval()", color="C1")
# ax.set_xticks(idx)
# ax.set_xlabel("позиція в рядку")
# ax.set_ylabel("значення")
# ax.set_title("Dropout: маска в train, як є в eval")
# ax.legend()
# fig.tight_layout()
# print("train mean", round(float(train_out.mean()), 3), "eval mean", round(float(eval_out.mean()), 3))
# plt.show()
# # -> train: нулі й двійки; eval: усі стовпці = 1

import torch
from torch import nn
import matplotlib.pyplot as plt

z = torch.linspace(-3, 3, 200).unsqueeze(1)
acts = {
    "ReLU": nn.ReLU(),
    "Tanh": nn.Tanh(),
    "LeakyReLU": nn.LeakyReLU(),
    "Swish": nn.SiLU(),
}
fig, ax = plt.subplots(figsize=(8, 4))
xs = z.numpy().ravel()
for i, (name, act) in enumerate(acts.items()):
    ys = act(z).detach().numpy().ravel()
    ax.plot(xs, ys, label=name, color=f"C{i}")
ax.axhline(0, color="0.7", linewidth=0.8)
ax.axvline(0, color="0.7", linewidth=0.8)
ax.set_xlabel("x")
ax.set_ylabel("act(x)")
ax.set_title("Один вхід — чотири форми")
ax.legend()
fig.tight_layout()
print("4 криві активацій")
# -> 4 криві на одному Axes
plt.show()