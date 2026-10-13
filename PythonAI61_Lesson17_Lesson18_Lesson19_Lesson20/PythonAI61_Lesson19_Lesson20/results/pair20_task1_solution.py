"""Пара 20 · завдання 1. EDA breast_cancer."""

from sklearn.datasets import load_breast_cancer

bunch = load_breast_cancer(as_frame=True)
print("shape", bunch.data.shape)
print(bunch.target.value_counts(normalize=True))
print(bunch.data.iloc[:, :5].describe().T[["mean", "std", "min", "max"]])
