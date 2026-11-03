"""Блок 9 · альтернатива з OPENAI_API_KEY (необов'язково).

Справжня модель отримує чотири питання. Подивіться, де контракт пройдено, а факт хибний.

Офлайн-версія: examples/example_09.py. Без ключа скрипт друкує «пропущено».
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

require_key()

chain = chain_with(live_json_model)
for question in ["Доставка Україною", "Самовивіз у Львові", "Марсіанський телепорт",
                 "Скільки коштує доставка у Варшаву?"]:
    docs = retrieve(question)
    try:
        result = chain.invoke(question)
    except Exception as exc:
        print(f"{question} → rejected: не JSON ({type(exc).__name__})")
        continue
    ok = validate_answer(result, docs)
    exact = isinstance(result, dict) and result.get("answer") in {d["text"] for d in docs} | {None}
    print(f"{question} → {result}\n   контракт: {ok} | дослівно з джерела: {exact}")
print_usage()
