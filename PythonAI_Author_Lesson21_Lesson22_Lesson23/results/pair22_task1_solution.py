"""Пара 22 · пункт 1. Сума вікна −27."""

window = [[0, 0, 9], [0, 0, 9], [0, 0, 9]]
kernel = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]
total = sum(window[i][j] * kernel[i][j] for i in range(3) for j in range(3))
assert total == -27
print(total)
