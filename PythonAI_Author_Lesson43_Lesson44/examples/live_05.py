"""Блок 5 · альтернатива з OPENAI_API_KEY (необов'язково).

Ручний граф станів answer → validate → stop, але відповідь дає справжня модель. Ліміт повторів задає програма.

Офлайн-версія: examples/example_05.py. Без ключа скрипт друкує «пропущено».
"""
from PythonAI_Author_Lesson43_Lesson44.live_openai import (
    chain_with, live_json_model, print_usage, require_key,
)
from PythonAI_Author_Lesson43_Lesson44.workshop import retrieve, validate_answer

require_key()

def run_docflow(question, max_attempts=2):
    state = {"question": question, "docs": retrieve(question), "log": []}
    chain = chain_with(live_json_model)
    node = "answer"
    while node != "stop":
        if node == "answer":
            try:
                state["answer"] = chain.invoke(question)
            except Exception as exc:  # зламаний JSON — теж стан, а не падіння
                state["answer"] = {"error": type(exc).__name__}
            node = "validate"
        elif node == "validate":
            ok = validate_answer(state["answer"], state["docs"])
            state["log"].append({"attempt": len(state["log"]) + 1, "valid": ok})
            node = "stop" if ok or len(state["log"]) >= max_attempts else "answer"
    return state

for question in ["Самовивіз у Львові", "Марсіанський телепорт"]:
    state = run_docflow(question)
    print(question, "→", state["answer"], state["log"])
print_usage()
