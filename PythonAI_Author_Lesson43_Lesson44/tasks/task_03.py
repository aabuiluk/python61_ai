"""**Завдання 3.** Розкладіть шість компонентів за шарами: сформувати prompt, знайти top-k,
викликати модель, перевірити JSON, обрати наступний tool, обмежити кроки.
Позначте, які вже реалізовані у 41–42, а які винесете в LCEL.

Підказки: 1. top-k — retrieval. 2. parser — етап chain. 3. tool selection та steps належать керуванню агентом.

Готово, якщо: Шість компонентів розкладено за шарами; є відповідність власному коду 41–42 і компонентам 44.

Окремі файли: examples/example_03.py і tasks/task_03.py у папці пакета.
Промпти для Gemini та ChatGPT — у PROMPTS.md.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Ваш код
# Напишіть власний розв’язок.
