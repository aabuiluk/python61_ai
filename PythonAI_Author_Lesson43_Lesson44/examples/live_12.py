"""Блок 12 · альтернатива з OPENAI_API_KEY (необов'язково).

DocFlow цілком: retrieval → prompt → справжня модель → parser → validate → журнал з токенами.

Офлайн-версія: examples/example_12.py. Без ключа скрипт друкує «пропущено».
"""
import json
from PythonAI_Author_Lesson43_Lesson44.live_openai import (
    chain_with, live_json_model, require_key, USAGE,
)
from PythonAI_Author_Lesson43_Lesson44.workshop import retrieve, validate_answer

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
