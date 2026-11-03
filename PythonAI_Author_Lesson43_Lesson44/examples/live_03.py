"""Блок 3 · альтернатива з OPENAI_API_KEY (необов'язково).

Шари ті самі: context → prompt → model → parser. Змінюється лише model-вузол: замість `fixture_model` стоїть `live_json_model`.

Офлайн-версія: examples/example_03.py. Без ключа скрипт друкує «пропущено».
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

require_key()

question = "Доставка Україною"
for name, model in [("fixture", RunnableLambda(fixture_model)), ("OpenAI", live_json_model)]:
    print(f"{name:8} →", chain_with(model).invoke(question))
print_usage()
