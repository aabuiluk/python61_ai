"""Пара 23 · відʼємна сума зникає, додатна лишається."""


def relu(value: float) -> float:
    return value if value > 0 else 0.0


print(relu(-27), relu(4), relu(0))
