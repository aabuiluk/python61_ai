"""Блок 4 · альтернатива з OPENAI_API_KEY (необов'язково).

Той самий запит двома способами: сирим OpenAI SDK без фреймворку і через LangChain-ланцюжок.

Офлайн-версія: examples/example_04.py. Без ключа скрипт друкує «пропущено».
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

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
