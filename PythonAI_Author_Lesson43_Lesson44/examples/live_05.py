"""Блок 5 · альтернатива з OPENAI_API_KEY (необов'язково).

Ручний граф станів answer → validate → stop, але відповідь дає справжня модель. Ліміт повторів задає програма.

Офлайн-версія: examples/example_05.py. Без ключа скрипт друкує «пропущено».
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

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
