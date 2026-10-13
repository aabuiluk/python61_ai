"""Пара 17 · завдання 2. ReLU MLP з/без Dropout."""

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


def run(dropout: bool):
    layers = [nn.Linear(10, 32), nn.ReLU()]
    if dropout:
        layers.append(nn.Dropout(0.3))
    layers.append(nn.Linear(32, 1))
    model = nn.Sequential(*layers)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    for _ in range(40):
        model.train()
        opt.zero_grad()
        nn.functional.mse_loss(model(x_tr), y_tr_t).backward()
        opt.step()
    model.eval()
    with torch.no_grad():
        pred = model(x_te).numpy().ravel()
    return mean_absolute_error(y_te, pred), r2_score(y_te, pred)

for flag in (False, True):
    mae, r2 = run(flag)
    print(("dropout" if flag else "plain"), round(mae, 3), round(r2, 3))
