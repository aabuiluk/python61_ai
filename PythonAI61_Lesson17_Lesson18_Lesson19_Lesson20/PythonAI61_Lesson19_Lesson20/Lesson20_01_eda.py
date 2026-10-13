"""Пара 20 · легко: огляд breast_cancer."""

from sklearn.datasets import load_breast_cancer
bunch = load_breast_cancer(as_frame=True)
print(bunch.data.shape)
print(bunch.target.value_counts())
