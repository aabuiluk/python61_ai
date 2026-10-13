"""Пара 17 · складніше: sklearn make_regression → тензори."""

import torch
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X, y = make_regression(200, 10, noise=10, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler().fit(X_tr)
x_tr = torch.tensor(scaler.transform(X_tr), dtype=torch.float32)
print(x_tr.shape, y_tr[:3])
