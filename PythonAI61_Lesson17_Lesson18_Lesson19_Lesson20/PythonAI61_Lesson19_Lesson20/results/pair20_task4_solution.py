"""Пара 20 · завдання 4. Метрики тесту."""

import torch
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch import nn

X, y = load_breast_cancer(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
sc = StandardScaler().fit(X_tr)
x_tr = torch.tensor(sc.transform(X_tr), dtype=torch.float32)
x_te = torch.tensor(sc.transform(X_te), dtype=torch.float32)
y_tr_t = torch.tensor(y_tr, dtype=torch.float32).view(-1, 1)
model = nn.Sequential(nn.Linear(30, 16), nn.ReLU(), nn.Linear(16, 1))
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.BCEWithLogitsLoss()
for _ in range(40):
    opt.zero_grad()
    loss_fn(model(x_tr), y_tr_t).backward()
    opt.step()
model.eval()
with torch.no_grad():
    pred = (torch.sigmoid(model(x_te)).numpy().ravel() >= 0.5).astype(int)
print("acc", round(accuracy_score(y_te, pred), 3))
print("prec", round(precision_score(y_te, pred), 3))
print("rec", round(recall_score(y_te, pred), 3))
print("Обмеження: немає клінічного контексту, одна вибірка sklearn, немає зовнішньої валідації.")
