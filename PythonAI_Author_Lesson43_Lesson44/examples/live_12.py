"""Блок 12 · альтернатива з OPENAI_API_KEY (необов'язково).

DocFlow цілком: retrieval → prompt → справжня модель → parser → validate → журнал з токенами.

Офлайн-версія: examples/example_12.py. Без ключа скрипт друкує «пропущено».
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

require_key()

chain = chain_with(live_json_model)
log = []
for question in ["Доставка Україною", "Марсіанський телепорт"]:
    docs = retrieve(question)
    result = chain.invoke(question)
    log.append({"question": question, "result": result,
                "valid": validate_answer(result, docs), "tokens": USAGE[-1]})
print(json.dumps(log, ensure_ascii=False, indent=2))
print("Офлайн-тести не змінились: make_chain() і далі використовує fixture_model.")
