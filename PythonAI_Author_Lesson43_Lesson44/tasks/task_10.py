"""**Завдання 10.** Створіть wrapper з двома сесіями. Надішліть два питання в A і одне в B.
Перевірте кількість повідомлень (4 і 2), порядок human/ai та відсутність тексту A
в історії B. Покажіть, що store є локальною пам’яттю процесу.

Підказки: 1. Новий store для вправи. 2. Окремий session_id у config. 3. Один invoke додає human та ai.

Готово, якщо: Сесія A має 4 повідомлення, B — 2; порядок human/ai збережено, витоку між сесіями немає.

Окремі файли: examples/example_10.py і tasks/task_10.py у папці пакета.
Промпти для Gemini та ChatGPT — у PROMPTS.md.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Ваш код
# Напишіть власний розв’язок.
