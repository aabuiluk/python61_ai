"""**Завдання 1.** Знайдіть один фрагмент про самовивіз у Львові, побудуйте JSON-контекст із id/text.
Перевірте пошук «Марсіанський телепорт» та порожній рядок. Поясніть значення score.

Підказки: 1. retrieve(question,1). 2. Виберіть id/text. 3. Невідомий словник і порожній запит мають дати [].

Готово, якщо: Знайдено pickup_lviv, є JSON-контекст, два порожні результати та пояснення score.

Окремі файли: examples/example_01.py і tasks/task_01.py у папці пакета.
Промпти для Gemini та ChatGPT — у PROMPTS.md.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Ваш код
# Напишіть власний розв’язок.
