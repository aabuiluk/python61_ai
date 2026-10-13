"""Пара 19 · завдання 2. Вихід і loss."""

print("binary   | Linear(h,1) | BCEWithLogitsLoss")
print("3-class  | Linear(h,3) | CrossEntropyLoss")
print("risk reg | Linear(h,1) | MSELoss")
print("BCEWithLogitsLoss = sigmoid+BCE в одному ядрі, стабільніше чисельно.")
