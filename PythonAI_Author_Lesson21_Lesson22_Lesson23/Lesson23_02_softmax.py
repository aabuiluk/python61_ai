"""Пара 23 · частки трьох класів у сумі дають 1."""

import math

scores = [1.0, 2.0, 3.0]
exps = [math.exp(score) for score in scores]
total = sum(exps)
shares = [item / total for item in exps]
print([round(item, 2) for item in shares])
print("sum", round(sum(shares), 6))
