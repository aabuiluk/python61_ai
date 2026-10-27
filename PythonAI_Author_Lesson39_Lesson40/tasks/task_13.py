"""**Завдання 13.** Створіть власну бібліотеку з чотирьох записів analytics, qa, content, code_review.
Використайте нові дані: продажі b01=4,b03=2; безкоштовна доставка від 800;
опис b03 за каталогом; дефект у def total(n): return 390-n.
Для кожного запишіть context, goal, format, prompt, version, acceptance.
Збережіть у results_39_40/prompt_library.json та перевірте контрольні очікування Python.

Підказки: 1. В QA перевірте 799/800/801. 2. Для code_review контракт — 390*n.
3. Аналітика має дати total=6, leader=b01. 4. У контенті не додавайте невідомого автора.

Критерій: Чотири повні промпти з шістьма полями; файл JSON; перевірені очікування аналітики, QA й коду.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Ваш код
# Напишіть власний код за умовою.

