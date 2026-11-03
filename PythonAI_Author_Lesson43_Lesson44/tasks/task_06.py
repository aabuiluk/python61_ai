"""**Завдання 6.** Попросіть модель написати чернетку ADR на інше питання: «Чи потрібен LlamaIndex для 3 правил магазину?». Перевірте, що в чернетці рівно 5 потрібних ключів, і надрукуйте рішення.

Підказки:
1. Змініть лише `question`.
2. Перевірка ключів: `set(draft) == REQUIRED`. Рішення: `draft["decision"]`.

Готово, якщо: Надруковано чернетку, `True`/`False` для ключів і рядок з рішенням. Ви погоджуєтесь або не погоджуєтесь з рішенням і пишете чому.

Подивіться examples/live_06.py — там той самий код без TODO. Потрібен OPENAI_API_KEY (див. README.md).
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

require_key()

# %% Ваш код: допишіть місця TODO
REQUIRED = {"context", "decision", "rejected", "risk", "acceptance"}
question = "Чи додавати LangGraph?"  # TODO 1: запитайте «Чи потрібен LlamaIndex для 3 правил магазину?»
prompt = ChatPromptTemplate.from_messages([
    ("system", "Ви пишете короткий ADR українською. Поверніть JSON рівно з ключами: "
               "context, decision, rejected, risk, acceptance."),
    ("human", "DocFlow: 3 локальні правила магазину, TF-IDF пошук, тести без мережі. {question}")])
draft = (prompt | live_json_model | JsonOutputParser()).invoke({"question": question})
print(json.dumps(draft, ensure_ascii=False, indent=2))
# TODO 2: надрукуйте, чи set(draft) == REQUIRED, і рішення draft["decision"]
