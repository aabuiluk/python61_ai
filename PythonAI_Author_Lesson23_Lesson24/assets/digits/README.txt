Локальний набір рукописних цифр 0–9 для пар 23–24.

digits_train.npz — ключі images (N,28,28) uint8, labels (N,) int64
digits_test.npz  — той самий контракт
png/digit_{0-9}_v{1-3}.png — по 3 варіанти на цифру для ручної перевірки

Нормалізація: mean/std рахуйте лише на train, test лише transform.
