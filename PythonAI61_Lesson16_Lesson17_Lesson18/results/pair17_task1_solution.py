"""Пара 17 · завдання 1. Активації MLP, MAE і R²."""

import torch
from sklearn.datasets import make_regression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch import nn

X, y = make_regression(2000, 10, noise=10, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
sc = StandardScaler().fit(X_tr)
x_tr = torch.tensor(sc.transform(X_tr), dtype=torch.float32)
x_te = torch.tensor(sc.transform(X_te), dtype=torch.float32)
y_tr_t = torch.tensor(y_tr, dtype=torch.float32).view(-1, 1)
y_te_np = y_te


def train_act(act):
    model = nn.Sequential(nn.Linear(10, 32), act, nn.Linear(32, 1))
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    for _ in range(40):
        opt.zero_grad()
        loss = nn.functional.mse_loss(model(x_tr), y_tr_t)
        loss.backward()
        opt.step()
    model.eval()
    with torch.no_grad():
        pred = model(x_te).numpy().ravel()
    return mean_absolute_error(y_te_np, pred), r2_score(y_te_np, pred)


for name, act in {
    "ReLU": nn.ReLU(),
    "Tanh": nn.Tanh(),
    "LeakyReLU": nn.LeakyReLU(),
    "Swish": nn.SiLU(),
}.items():
    mae, r2 = train_act(act)
    print(f"{name:10} MAE={mae:.3f} R2={r2:.3f}")
