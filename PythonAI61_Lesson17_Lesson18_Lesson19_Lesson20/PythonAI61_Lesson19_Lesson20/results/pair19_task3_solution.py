# """Пара 19 · завдання 3. 8 шарів Sigmoid vs ReLU."""
#
# import torch
# from sklearn.datasets import make_regression
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from torch import nn
#
# X, y = make_regression(800, 10, noise=8, random_state=0)
# X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.2, random_state=0)
# x = torch.tensor(StandardScaler().fit_transform(X_tr), dtype=torch.float32)
# yt = torch.tensor(y_tr, dtype=torch.float32).view(-1, 1)
#
#
# def make(act):
#     layers: list[nn.Module] = [nn.Linear(10, 16), act()]
#     for _ in range(7):
#         layers += [nn.Linear(16, 16), act()]
#     layers.append(nn.Linear(16, 1))
#     return nn.Sequential(*layers)
#
#
# def fit(act):
#     model = make(act)
#     opt = torch.optim.SGD(model.parameters(), lr=0.001)
#     last = None
#     for _ in range(30):
#         opt.zero_grad()
#         loss = nn.functional.mse_loss(model(x), yt)
#         if not torch.isfinite(loss):
#             return float("nan")
#         loss.backward()
#         opt.step()
#         last = float(loss)
#     return last
#
# print("sigmoid", fit(nn.Sigmoid), "relu", fit(nn.ReLU))

import torch
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch import nn

X, y = make_regression(800, 10, noise=8, random_state=0)
X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.2, random_state=0)
x = torch.tensor(StandardScaler().fit_transform(X_tr), dtype=torch.float32)
yt = torch.tensor(y_tr, dtype=torch.float32).view(-1, 1)


def make(act):
  layers: list[nn.Module] = [
      nn.Linear(10, 16),
      nn.BatchNorm1d(16),
      act(),
  ]
  for _ in range(7):
    layers += [nn.Linear(16, 16), nn.BatchNorm1d(16), act()]
  layers.append(nn.Linear(16, 1))
  return nn.Sequential(*layers)


def fit(act):
  model = make(act)
  opt = torch.optim.SGD(model.parameters(), lr=0.001)
  last = None
  for _ in range(30):
    opt.zero_grad()
    loss = nn.functional.mse_loss(model(x), yt)
    if not torch.isfinite(loss):
      return float("nan")
    loss.backward()
    opt.step()
    last = float(loss)
  return last


print("sigmoid", fit(nn.Sigmoid), "relu", fit(nn.ReLU))