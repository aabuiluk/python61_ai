"""Пара 22 · пункт 3. Другий шар: 144 і 4608, сторона карти 30."""

one_kernel = 3 * 3 * 16
layer = one_kernel * 32
side = (32 + 2 * 0 - 3) // 1 + 1
assert one_kernel == 144
assert layer == 4608
assert side == 30
print(one_kernel, layer, side)
