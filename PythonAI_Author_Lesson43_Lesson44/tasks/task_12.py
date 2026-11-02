"""**Завдання 12.** Запустіть DocFlow для доставки, самовивозу й невідомого факту. Створіть звіт із
question, answer, sources, passed, mode. Для відомих питань перевірте точний текст
першого документа; для невідомого — null/[]. Збережіть results_43_44/report.json.
Додайте один негативний кейс невідомого source id. Напишіть два речення про межі fixtures.

Підказки: 1. Для кожного питання повторно отримайте docs. 2. passed об’єднує контракт і очікуваний факт. 3. mode завжди fixture, не live.

Готово, якщо: Три кейси пройшли контракт і точну перевірку; негативний id відхилено; JSON-звіт має mode=fixture й чесний висновок.

Окремі файли: examples/example_12.py і tasks/task_12.py у папці пакета.
Промпти для Gemini та ChatGPT — у PROMPTS.md.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Ваш код
# Напишіть власний розв’язок.
