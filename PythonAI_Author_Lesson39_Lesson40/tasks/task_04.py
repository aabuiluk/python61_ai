"""**Завдання 4.** Напишіть dispatch(request) з allowlist для lookup_book.
Перевірте b02, b99 і недозволену дію delete_all. Складіть журнал request → observation
для двох дозволених пошуків. Після None відповідь має повідомити, що запис відсутній.

Підказки: 1. Перевірте набір ключів і назву action. 2. Пошук зробіть через next(..., None).
3. Для delete_all перехопіть ValueError; не реалізуйте цю дію.

Критерій: b02 → 450; b99 → None; delete_all заблокована; журнал містить реальні результати Python.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Ваш код
# Напишіть власний код за умовою.

