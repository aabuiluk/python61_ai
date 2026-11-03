"""Блок 2 · альтернатива з OPENAI_API_KEY (необов'язково).

Тепер рішення «викликати інструмент» ухвалює справжня модель. Allowlist, ліміт кроків і журнал лишаються в нашому коді.

Офлайн-версія: examples/example_02.py. Без ключа скрипт друкує «пропущено».
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

require_key()

tools = [{"type": "function", "name": "search_knowledge", "strict": True,
          "description": "Пошук у правилах магазину. Повертає фрагменти з id.",
          "parameters": {"type": "object", "additionalProperties": False,
                         "properties": {"question": {"type": "string"}}, "required": ["question"]}}]
ALLOWED = {"search_knowledge"}
messages = [{"role": "user", "content": "Скільки коштує доставка Україною? Відповідай лише за знайденими правилами."}]
trace = []
for step in range(1, 4):  # ліміт кроків
    response = client().responses.create(model=MODEL, input=messages, tools=tools,
                                          store=False, max_output_tokens=300)
    record_usage(response)
    calls = [item for item in response.output if item.type == "function_call"]
    if not calls:
        print("Відповідь моделі:", response.output_text)
        break
    for call in calls:
        if call.name not in ALLOWED:
            raise ValueError("Невідомий tool: " + call.name)
        arguments = json.loads(call.arguments)
        observation = retrieve(arguments["question"], 1)
        trace.append({"step": step, "arguments": arguments, "observation": [h["id"] for h in observation]})
        messages += [{"type": "function_call", "call_id": call.call_id, "name": call.name, "arguments": call.arguments},
                     {"type": "function_call_output", "call_id": call.call_id,
                      "output": json.dumps(observation, ensure_ascii=False)}]
print(json.dumps(trace, ensure_ascii=False, indent=2))
print_usage()
