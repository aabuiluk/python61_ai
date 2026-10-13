"""Пара 23 · пункт 1. ReLU."""


def relu(value: float) -> float:
    return value if value > 0 else 0.0


assert relu(-27) == 0
assert relu(4) == 4
assert relu(0) == 0
print(relu(-27), relu(4), relu(0))
