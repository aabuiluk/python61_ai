"""Блок 9 · альтернатива з OPENAI_API_KEY (необов'язково).

Справжня модель отримує чотири питання. Подивіться, де контракт пройдено, а факт хибний.

Офлайн-версія: examples/example_09.py. Без ключа скрипт друкує «пропущено».
"""
from PythonAI_Author_Lesson43_Lesson44.live_openai import (
    chain_with, live_json_model, print_usage, require_key,
)
from PythonAI_Author_Lesson43_Lesson44.workshop import retrieve, validate_answer

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
