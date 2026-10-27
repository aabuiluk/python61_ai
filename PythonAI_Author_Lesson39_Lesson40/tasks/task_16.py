"""**Завдання 16.** Створіть чотири кейси: правильна b01, неправильна ціна b02,
невідомий id, не-JSON. Побудуйте звіт з case_id, prompt_version, model, mode, passed, response.
Збережіть у results_39_40/eval_report.csv. Очікуйте один прийнятий кейс із чотирьох.
Напишіть два речення про те, що виміряли та чого цей експеримент не показує.

Підказки: 1. model для ручних відповідей — none. 2. Створіть папку через mkdir(exist_ok=True).
3. csv.DictWriter записує header і всі рядки. 4. У звіті збережіть також неправильні відповіді.

Критерій: CSV має 4 рядки даних; passed=True один раз; mode=fixture та model=none.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Ваш код
# Напишіть власний код за умовою.

