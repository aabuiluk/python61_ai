"""Пара 18 · завдання 4. Зведена таблиця чотирьох MLP."""

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


def build(kind: str) -> nn.Module:
    layers = [nn.Linear(10, 32)]
    if "bn" in kind:
        layers.append(nn.BatchNorm1d(32))
    layers.append(nn.ReLU())
    if "drop" in kind:
        layers.append(nn.Dropout(0.3))
    layers.append(nn.Linear(32, 1))
    return nn.Sequential(*layers)


def eval_kind(kind: str):
    model = build(kind)
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

print(f"{'config':<16} {'MAE':>8} {'R2':>8}")
for kind, label in [("relu", "ReLU"), ("relu_drop", "ReLU+Dropout"), ("relu_bn", "ReLU+BN"), ("relu_bn_drop", "all")]:
    mae, r2 = eval_kind(kind)
    print(f"{label:<16} {mae:8.3f} {r2:8.3f}")
print("Висновок: BatchNorm зазвичай стабілізує масштаб; Dropout корисний, якщо train сильно кращий за test.")
