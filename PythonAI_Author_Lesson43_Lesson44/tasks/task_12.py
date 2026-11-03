"""**Завдання 12.** Зберіть функцію `docflow(question)`, яка повертає один запис журналу: питання, answer, sources, valid і токени. Запустіть її на двох питаннях.

Підказки:
1. `result` — це словник з `answer` і `sources`.
2. Токени останнього виклику: `USAGE[-1]`.
3. Порівняйте з `examples/live_12.py`.

Готово, якщо: Для двох питань надруковано записи з п'ятьма ключами. Для «Марсіанського телепорту» `answer` = `null`, `valid` = `true`.

Подивіться examples/live_12.py — там той самий код без TODO. Потрібен OPENAI_API_KEY (див. README.md).
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

require_key()

# %% Ваш код: допишіть місця TODO
chain = chain_with(live_json_model)

def docflow(question):
    docs = retrieve(question)
    result = chain.invoke(question)
    # TODO: поверніть словник з ключами question, answer, sources, valid, tokens
    return {"question": question, "result": result}

for question in ["Доставка Україною", "Марсіанський телепорт"]:
    print(json.dumps(docflow(question), ensure_ascii=False, indent=2))
