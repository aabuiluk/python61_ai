"""Блок 3 · альтернатива з OPENAI_API_KEY (необов'язково).

Шари ті самі: context → prompt → model → parser. Змінюється лише model-вузол: замість `fixture_model` стоїть `live_json_model`.

Офлайн-версія: examples/example_03.py. Без ключа скрипт друкує «пропущено».
"""
from langchain_core.runnables import RunnableLambda
from PythonAI_Author_Lesson43_Lesson44.live_openai import (
    chain_with, live_json_model, print_usage, require_key,
)
from PythonAI_Author_Lesson43_Lesson44.workshop import fixture_model

require_key()

question = "Доставка Україною"
for name, model in [("fixture", RunnableLambda(fixture_model)), ("OpenAI", live_json_model)]:
    print(f"{name:8} →", chain_with(model).invoke(question))
print_usage()
