"""Пара 22 · пункт 2. Рівне поле дає 0."""

window = [[4, 4, 4], [4, 4, 4], [4, 4, 4]]
kernel = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]
total = sum(window[i][j] * kernel[i][j] for i in range(3) for j in range(3))
assert total == 0
print(total)
