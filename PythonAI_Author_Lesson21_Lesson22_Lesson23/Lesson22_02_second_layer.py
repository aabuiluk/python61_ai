"""Пара 22 · друге ядро дивиться на всі карти попереднього шару."""

one_kernel = 3 * 3 * 16
layer = one_kernel * 32
side = (32 - 3) // 1 + 1
print("one kernel", one_kernel)
print("layer", layer)
print("map side without padding", side)
