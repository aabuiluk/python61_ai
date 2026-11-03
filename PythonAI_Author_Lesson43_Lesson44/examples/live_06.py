"""Блок 6 · альтернатива з OPENAI_API_KEY (необов'язково).

Модель може запропонувати чернетку ADR. Перевірку форми робить код, а рішення ухвалює команда.

Офлайн-версія: examples/example_06.py. Без ключа скрипт друкує «пропущено».
"""
import json
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from PythonAI_Author_Lesson43_Lesson44.live_openai import live_json_model, print_usage, require_key

require_key()

REQUIRED = {"context", "decision", "rejected", "risk", "acceptance"}
prompt = ChatPromptTemplate.from_messages([
    ("system", "Ви пишете короткий ADR українською. Поверніть JSON рівно з ключами: "
               "context, decision, rejected, risk, acceptance."),
    ("human", "DocFlow: 3 локальні правила магазину, TF-IDF пошук, відповідь JSON з джерелами, "
              "тести без мережі. Чи додавати LangGraph і LlamaIndex?")])
draft = (prompt | live_json_model | JsonOutputParser()).invoke({})
print(json.dumps(draft, ensure_ascii=False, indent=2))
print("Ключі збігаються:", set(draft) == REQUIRED)
print_usage()
