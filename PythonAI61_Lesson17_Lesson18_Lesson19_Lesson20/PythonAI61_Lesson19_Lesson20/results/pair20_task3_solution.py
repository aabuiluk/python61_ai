"""Пара 20 · завдання 3. MLP + BCEWithLogits."""

import torch
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch import nn

X, y = load_breast_cancer(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
sc = StandardScaler().fit(X_tr)
x_tr = torch.tensor(sc.transform(X_tr), dtype=torch.float32)
y_tr_t = torch.tensor(y_tr, dtype=torch.float32).view(-1, 1)
model = nn.Sequential(nn.Linear(30, 16), nn.ReLU(), nn.Linear(16, 1))
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.BCEWithLogitsLoss()
for _ in range(40):
    opt.zero_grad()
    loss = loss_fn(model(x_tr), y_tr_t)
    loss.backward()
    opt.step()
print("final train loss", float(loss))
torch.save(model.state_dict(), "heart_mlp.pt")
print("saved heart_mlp.pt")
