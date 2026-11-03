"""**Завдання 5.** Зробіть цикл повторів: викликайте ланцюжок, доки відповідь не пройде `validate_answer`, але не більше 2 разів. Перевірте на «Самовивіз у Львові» і на «Марсіанський телепорт».

Підказки:
1. Зупинити цикл можна через `break`, коли `ok` дорівнює `True`.
2. Ліміт уже задано в `range(1, max_attempts + 1)`: модель не вирішує, скільки разів повторювати.

Готово, якщо: Для кожного питання надруковано не більше 2 спроб. Після першої валідної відповіді цикл зупиняється.

Подивіться examples/live_05.py — там той самий код без TODO. Потрібен OPENAI_API_KEY (див. README.md).
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

require_key()

# %% Ваш код: допишіть місця TODO
chain = chain_with(live_json_model)
max_attempts = 2
question = "Самовивіз у Львові"  # потім змініть на "Марсіанський телепорт"
docs = retrieve(question)
for attempt in range(1, max_attempts + 1):
    result = chain.invoke(question)
    ok = validate_answer(result, docs)
    print(f"Спроба {attempt}: {result} → valid={ok}")
    # TODO: якщо ok — зупиніть цикл
print_usage()
