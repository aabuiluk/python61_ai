"""Пара 20 · завдання 2. Split і scaler."""

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
sc = StandardScaler().fit(X_tr)
print("train mean", sc.transform(X_tr).mean().round(4))
print("test mean", sc.transform(X_te).mean().round(4))
print("sizes", X_tr.shape, X_te.shape)
