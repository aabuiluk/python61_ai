"""**Завдання 2.** Запустіть агентний цикл з `examples/live_02.py` на своєму питанні: о котрій відкривається магазин. Додайте перевірку allowlist: якщо модель викликала інструмент не зі списку `ALLOWED`, програма зупиняється з помилкою.

Підказки:
1. Змініть лише `question`, решта циклу вже готова.
2. Перевірка — два рядки: `if call.name not in ALLOWED:` і `raise ValueError(...)`.
3. Якщо observation порожній, TF-IDF не знайшов слів моделі. Це видно в `arguments`.

Готово, якщо: У `trace` є крок з `search_knowledge` і його `arguments`. Модель відповідає «09:00» або чесно каже, що не знайшла правила.

Подивіться examples/live_02.py — там той самий код без TODO. Потрібен OPENAI_API_KEY (див. README.md).
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

require_key()

# %% Ваш код: допишіть місця TODO
tools = [{"type": "function", "name": "search_knowledge", "strict": True,
          "description": "Пошук у правилах магазину. Повертає фрагменти з id.",
          "parameters": {"type": "object", "additionalProperties": False,
                         "properties": {"question": {"type": "string"}}, "required": ["question"]}}]
ALLOWED = {"search_knowledge"}
question = "Скільки коштує доставка Україною?"  # TODO 1: запитайте, о котрій відкривається магазин
messages = [{"role": "user", "content": question + " Відповідай лише за знайденими правилами."}]
trace = []
for step in range(1, 4):  # не більше 3 кроків
    response = client().responses.create(model=MODEL, input=messages, tools=tools,
                                          store=False, max_output_tokens=300)
    record_usage(response)
    calls = [item for item in response.output if item.type == "function_call"]
    if not calls:
        print("Відповідь моделі:", response.output_text)
        break
    for call in calls:
        # TODO 2: якщо call.name немає в ALLOWED — raise ValueError("Невідомий tool: " + call.name)
        arguments = json.loads(call.arguments)
        observation = retrieve(arguments["question"], 1)
        trace.append({"step": step, "arguments": arguments, "observation": [h["id"] for h in observation]})
        messages += [{"type": "function_call", "call_id": call.call_id, "name": call.name, "arguments": call.arguments},
                     {"type": "function_call_output", "call_id": call.call_id,
                      "output": json.dumps(observation, ensure_ascii=False)}]
print(json.dumps(trace, ensure_ascii=False, indent=2))
