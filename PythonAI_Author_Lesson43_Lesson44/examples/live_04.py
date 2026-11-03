"""Блок 4 · альтернатива з OPENAI_API_KEY (необов'язково).

Той самий запит двома способами: сирим OpenAI SDK без фреймворку і через LangChain-ланцюжок.

Офлайн-версія: examples/example_04.py. Без ключа скрипт друкує «пропущено».
"""
import json
from PythonAI_Author_Lesson43_Lesson44.live_openai import (
    chain_with, client, live_json_model, MODEL, print_usage, record_usage, require_key,
)
from PythonAI_Author_Lesson43_Lesson44.workshop import context_for

require_key()

question = "Доставка Україною"
context = context_for(question)
response = client().responses.create(
    model=MODEL, store=False, max_output_tokens=200,
    text={"format": {"type": "json_object"}},
    input=[{"role": "system", "content": "Працюйте лише за контекстом. Поверніть answer та sources у JSON."},
           {"role": "user", "content": f"<context>{context}</context>\nПитання: {question}"}])
record_usage(response)
print("Сирий SDK:", json.loads(response.output_text))
print("LangChain:", chain_with(live_json_model).invoke(question))
print_usage()
