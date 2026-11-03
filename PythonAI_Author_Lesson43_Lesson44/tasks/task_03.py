"""**Завдання 3.** Запустіть той самий DocFlow-ланцюжок двічі: з `fixture_model` і з OpenAI. Порівняйте відповіді на трьох питаннях.

Підказки:
1. `chain_with(model)` уже складає context → prompt → model → parser.
2. Потрібен один рядок у циклі: `print("  OpenAI: ", openai_chain.invoke(question))`.

Готово, якщо: Для кожного з трьох питань надруковано дві відповіді. Ви записали, де вони відрізняються (текст, кількість джерел, відмова).

Подивіться examples/live_03.py — там той самий код без TODO. Потрібен OPENAI_API_KEY (див. README.md).
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

require_key()

# %% Ваш код: допишіть місця TODO
questions = ["Доставка Україною", "Самовивіз у Львові", "Марсіанський телепорт"]
fixture_chain = chain_with(RunnableLambda(fixture_model))
openai_chain = chain_with(live_json_model)
for question in questions:
    print(question)
    print("  fixture:", fixture_chain.invoke(question))
    # TODO: надрукуйте відповідь openai_chain на це саме питання
print_usage()
