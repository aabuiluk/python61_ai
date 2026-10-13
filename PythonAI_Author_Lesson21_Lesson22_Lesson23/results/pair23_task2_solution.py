"""Пара 23 · пункт 2. Softmax для рахунків 1, 2, 3."""

import math

scores = [1.0, 2.0, 3.0]
exps = [math.exp(score) for score in scores]
total = sum(exps)
shares = [item / total for item in exps]
assert abs(sum(shares) - 1) < 1e-9
assert shares[2] == max(shares)
print([round(item, 2) for item in shares])
