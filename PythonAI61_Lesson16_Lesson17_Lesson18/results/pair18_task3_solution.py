"""Пара 18 · завдання 3. BatchNorm, графік loss."""

from pathlib import Path

import matplotlib.pyplot as plt
import torch
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch import nn

X, y = make_regression(2000, 10, noise=10, random_state=42)
X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.2, random_state=42)
sc = StandardScaler().fit(X_tr)
x = torch.tensor(sc.transform(X_tr), dtype=torch.float32)
yt = torch.tensor(y_tr, dtype=torch.float32).view(-1, 1)
model = nn.Sequential(nn.Linear(10, 32), nn.BatchNorm1d(32), nn.ReLU(), nn.Linear(32, 1))
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
hist = []
for _ in range(40):
    model.train()
    opt.zero_grad()
    loss = nn.functional.mse_loss(model(x), yt)
    loss.backward()
    opt.step()
    hist.append(float(loss))
plt.plot(hist)
plt.xlabel("epoch")
plt.ylabel("MSE")
out = Path(__file__).with_suffix(".png")
plt.savefig(out, dpi=120, bbox_inches="tight")
print("saved", out, "final", hist[-1])
