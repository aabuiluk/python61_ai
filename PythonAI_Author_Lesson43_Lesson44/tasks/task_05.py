"""**Завдання 5.** Опишіть маршрут DocFlow з одним repair і трьома ролями. Для кожної ролі задайте
вхід і вихід; для процесу — max_repairs=1 та кінцевий stop. Поясніть, коли обрали б
явний граф станів, а коли організацію співпраці ролей.

Підказки: 1. Результат researcher — документи з id. 2. Editor не вигадує джерел. 3. Reviewer повертає дефекти, а не автоматичну істину.

Готово, якщо: Три ролі з контрактами, один repair і кінцевий stop; пояснено два стилі організації.

Окремі файли: examples/example_05.py і tasks/task_05.py у папці пакета.
Промпти для Gemini та ChatGPT — у PROMPTS.md.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Ваш код
# Напишіть власний розв’язок.
